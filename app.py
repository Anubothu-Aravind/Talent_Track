import streamlit as st
import os
import io
import base64
import PyPDF2 as pdf
import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

# Configure Gemini API with direct key
GEMINI_API_KEY = "AIzaSyCJf1-6hUM0jdm0LdfL-yhKI6d5bcUSfcs"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_gemini_response(input_prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input_prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

def input_pdf_setup(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def extract_sections(text):
    """Extract different sections from the resume"""
    sections = {
        'skills': '',
        'education': '',
        'experience': '',
        'summary': ''
    }
    
    # Simple rule-based section extraction
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip().lower()
        if 'skills' in line or 'technical skills' in line:
            current_section = 'skills'
        elif 'education' in line or 'academic' in line:
            current_section = 'education'
        elif 'experience' in line or 'work history' in line:
            current_section = 'experience'
        elif 'summary' in line or 'objective' in line:
            current_section = 'summary'
        elif current_section and line:
            sections[current_section] += line + ' '
    
    return sections

def calculate_section_relevance(section_text, job_description):
    """Calculate relevance score for a section against job description"""
    if not section_text.strip():
        return 0.0
    
    # Get embeddings
    section_embedding = model.encode([section_text])
    jd_embedding = model.encode([job_description])
    
    # Calculate cosine similarity
    similarity = cosine_similarity(section_embedding, jd_embedding)[0][0]
    return float(similarity)

def rank_cv_sections(resume_text, job_description):
    """Rank different sections of a CV based on relevance to job description"""
    sections = extract_sections(resume_text)
    section_scores = {}
    
    for section_name, section_text in sections.items():
        score = calculate_section_relevance(section_text, job_description)
        section_scores[section_name] = score
    
    # Sort sections by score
    ranked_sections = sorted(section_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_sections

def rank_multiple_cvs(cv_texts, job_description):
    """Rank multiple CVs based on overall relevance to job description"""
    cv_scores = []
    
    for i, cv_text in enumerate(cv_texts):
        sections = extract_sections(cv_text)
        section_scores = []
        
        for section_text in sections.values():
            score = calculate_section_relevance(section_text, job_description)
            section_scores.append(score)
        
        # Calculate overall CV score (average of section scores)
        overall_score = np.mean(section_scores)
        cv_scores.append((i, overall_score))
    
    # Sort CVs by score
    ranked_cvs = sorted(cv_scores, key=lambda x: x[1], reverse=True)
    return ranked_cvs

# Streamlit UI
st.set_page_config(page_title="TalentTrack")
st.title("TalentTrack: ATS Tracking System")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f4f4f4;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50; /* Green */
        border: none;
        color: white;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextArea {
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 10px;
    }
    .stFileUploader>label {
        font-weight: bold;
        font-size: 16px;
    }
    .stSpinner {
        margin: auto;
        border: 4px solid #f3f3f3;
        border-block-start: 4px solid #3498db;
        border-radius: 50%;
        inline-size: 40px;
        block-size: 40px;
        animation: spin 2s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

job_description = st.text_area("Job Description:", key="input", height=200)
uploaded_files = st.file_uploader("Upload your resume(s) (PDF)...", type=["pdf"], accept_multiple_files=True)

resume_texts = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.success(f"PDF '{uploaded_file.name}' Uploaded Successfully")
        resume_text = input_pdf_setup(uploaded_file)
        if resume_text:
            resume_texts.append(resume_text)

col1, col2, col3, col4 = st.columns(4)

with col1:
    submit1 = st.button("Analyze Resume")
with col2:
    submit2 = st.button("Suggest Improvements")
with col3:
    submit3 = st.button("Match Percentage")
with col4:
    submit4 = st.button("Rank CVs")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Review the provided resume against the job description. 
Provide a professional evaluation addressing:
1. Overall alignment of the candidate's profile with the role
2. Key strengths that match the requirements
3. Areas where the candidate's profile could be stronger
4. Final recommendation

Resume: {text}
Job Description: {jd}

Provide the analysis in a clear, structured format with bullet points for each section.
"""

input_prompt2 = """
You are a career coach specializing in technical roles. Based on the provided resume and job description, provide:
1. Specific skills or qualifications the candidate should add
2. Suggestions for improving existing experience descriptions
3. Recommended certifications or training
4. Resources for skill development
5. Tips for better alignment with the job requirements

Resume: {text}
Job Description: {jd}

Present your suggestions in a structured format with clear headings and bullet points.
"""

input_prompt3 = """
You are an ATS (Applicant Tracking System) expert. Analyze the resume against the job description and provide:
1. Overall match percentage (give a specific number)
2. Key matching keywords found
3. Important keywords missing from the resume
4. Specific suggestions for ATS optimization
5. Final recommendations for improvement

Resume: {text}
Job Description: {jd}

Present the analysis in a clear format with sections and bullet points. For the match percentage, provide a specific number between 0-100.
"""

if submit1 or submit2 or submit3 or submit4:
    if not job_description:
        st.error("Please enter a job description.")
    elif not resume_texts:
        st.error("Please upload at least one resume in PDF format.")
    else:
        with st.spinner():
            try:
                if submit1:
                    st.subheader("Resume Analysis")
                    formatted_prompt = input_prompt1.format(text=resume_texts[0], jd=job_description)
                    response = get_gemini_response(formatted_prompt)
                    if response:
                        st.write(response)
                    
                elif submit2:
                    st.subheader("Improvement Suggestions")
                    formatted_prompt = input_prompt2.format(text=resume_texts[0], jd=job_description)
                    response = get_gemini_response(formatted_prompt)
                    if response:
                        st.write(response)
                    
                elif submit3:
                    st.subheader("Match Percentage and Keywords")
                    formatted_prompt = input_prompt3.format(text=resume_texts[0], jd=job_description)
                    response = get_gemini_response(formatted_prompt)
                    if response:
                        st.write(response)
                    
                elif submit4:
                    st.subheader("CV Rankings")
                    
                    # First, show section-wise ranking for the first CV
                    st.write("### Section-wise Ranking (First CV)")
                    section_rankings = rank_cv_sections(resume_texts[0], job_description)
                    for section, score in section_rankings:
                        st.write(f"{section.title()}: {score:.2f}")
                    
                    # Then, show overall ranking of all CVs
                    if len(resume_texts) > 1:
                        st.write("### Overall CV Rankings")
                        cv_rankings = rank_multiple_cvs(resume_texts, job_description)
                        for i, (cv_index, score) in enumerate(cv_rankings, 1):
                            st.write(f"Rank {i}: CV {cv_index + 1} (Score: {score:.2f})")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.error("Please try again. If the error persists, check your API key configuration.")
