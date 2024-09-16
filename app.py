from http.client import responses

import streamlit as st
import os
import io
import base64
from PIL import Image
import PyPDF2 as pdf
import google.generativeai as genai
from dotenv import load_dotenv

# load_dotenv()

genai.configure(api_key="AIzaSyDElTmuLbMW3E65nGN-80DXlHl8nuB9Nk4")


def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_prompt)
    return response.text


def input_pdf_setup(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    print(text)
    return text



st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
Resume: {text}
Description: {jd}
"""

input_prompt2 = """
You are a highly experienced career coach with expertise in technical roles. Your task is to provide specific feedback 
on how the candidate can improve their skills and qualifications based on the provided resume and job description. 
Identify key areas where the candidate's skills may be lacking or could be enhanced. Offer suggestions for additional 
skills or certifications they should consider, and recommend relevant resources or strategies for improvement.
Also, indicate how the candidate can better align their profile with the job description to increase their chances of success.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        resume_text = input_pdf_setup(uploaded_file)
        formatted_prompt = input_prompt1.format(text=resume_text, jd=input_text)
        response = get_gemini_response(formatted_prompt)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        resume_text = input_pdf_setup(uploaded_file)
        formatted_prompt = input_prompt3.format(text=resume_text, jd=input_text)
        response = get_gemini_response(formatted_prompt)
        st.subheader("The Response is")
        st.write(response)

elif submit3:
    if uploaded_file is not None:
        resume_text = input_pdf_setup(uploaded_file)
        formatted_prompt = input_prompt3.format(text=resume_text, jd=input_text)
        response = get_gemini_response(formatted_prompt)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")