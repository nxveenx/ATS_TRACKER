import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(text, jd):
    input_prompt = f"""
    Hey Act Like a skilled or very experienced ATS(Application Tracking System)
    with a deep understanding of the tech field, software engineering, data science, data analyst,
    and big data engineer. Your task is to evaluate the resume based on the given job description.
    You must consider that the job market is very competitive, and you should provide 
    the best assistance for improving the resumes. Assign the percentage Matching based 
    on JD and the missing keywords with high accuracy.
    resume: {text}
    description: {jd}

    I want the response in one single string having the structure
    {{"JD Match":"%", "MissingKeywords":[], "Profile Summary":""}}
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Streamlit app

st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(text, jd)
        st.subheader(response)
