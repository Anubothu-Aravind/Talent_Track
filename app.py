import streamlit as st
import os
import io
import base64
import PyPDF2 as pdf
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

# Configure Gemini API
#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key="AIzaSyDElTmuLbMW3E65nGN-80DXlHl8nuB9Nk4")

def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(input_prompt)
    return response.text

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

# Set page config
st.set_page_config(page_title="TalentTrack")
st.title("TalentTrack: ATS Tracking System")

job_description = st.text_area("Job Description:", key="input", height=200)
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

resume_text = None
if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")
    resume_text = input_pdf_setup(uploaded_file)

col1, col2, col3 = st.columns(3)

with col1:
    submit1 = st.button("Analyze Resume")
with col2:
    submit2 = st.button("Suggest Improvements")
with col3:
    submit3 = st.button("Match Percentage")

input_prompt1 = """
As an experienced Technical Human Resource Manager, review the provided resume against the job description. 
Share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
Resume: {text}
Description: {jd}
"""

input_prompt2 = """
As a highly experienced career coach with expertise in technical roles, provide specific feedback 
on how the candidate can improve their skills and qualifications based on the provided resume and job description. 
Identify key areas for improvement, suggest additional skills or certifications, and recommend relevant resources or strategies.
Indicate how the candidate can better align their profile with the job description to increase their chances of success.
Resume: {text}
Description: {jd}
"""

input_prompt3 = """
As a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
evaluate the resume against the provided job description. Provide:
1. The percentage match between the resume and job description
2. Keywords missing from the resume
3. Final thoughts and recommendations
Resume: {text}
Description: {jd}
"""

if submit1 or submit2 or submit3:
    with st.spinner("Analyzing..."):
        if resume_text is None:
            st.error("Please upload a resume in PDF format.")
        else:
            if submit1:
                prompt = input_prompt1
                subheader = "Resume Analysis"
            elif submit2:
                prompt = input_prompt2
                subheader = "Improvement Suggestions"
            else:
                prompt = input_prompt3
                subheader = "Match Percentage and Keywords"

            formatted_prompt = prompt.format(text=resume_text, jd=job_description)
            response = get_gemini_response(formatted_prompt)

            if response:
                st.subheader(subheader)
                st.write(response)
            else:
                st.error("Failed to generate a response. Please try again.")
