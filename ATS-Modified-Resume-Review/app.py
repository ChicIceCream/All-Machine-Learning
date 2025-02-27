from dotenv import load_dotenv
load_dotenv()

from google import generativeai as genai
import streamlit as st
import os
import PyPDF2 as pdf

# configure my api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# define my function to call the api

def get_gemini_response(input, resume, prompt):
    # Define my model here as flash model 
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # calling my model
    response = model.generate_content([input, resume, prompt])
    
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

analyze_prompt = '''
"Analyze the content of my resume. Provide a detailed breakdown of my strengths, key skills, and qualifications, based on the information in the resume. Highlight the areas where I stand out, and how my experience aligns with general industry standards."
'''
improvement_prompt = '''
Review my resume and suggest specific improvements to make it more effective. Identify gaps in skills, experience, or presentation that could enhance my chances in the job market. Provide actionable recommendations for better structure, clarity, or any other areas that can be optimized.
'''
keyword_prompt = '''
Scan my resume for important keywords and industry-specific terms related to my field or target job description. Identify any crucial keywords or phrases that are missing and explain how incorporating them could make my resume more attractive to potential employers and Applicant Tracking Systems (ATS).
'''
percentage_prompt = '''
Compare my resume to the provided job description and calculate a percentage match. Analyze how well my skills, experience, and qualifications align with the requirements of the job. Highlight the areas where I meet the criteria and those where I fall short, with suggestions to improve alignment
'''
## Streamlit app

st.title("ATS Resume Reviewer")
st.text("Improve your resume")
jd = st.text_area("Paste the job description over here")
uploaded_file = st.file_uploader("Upload your resume here", type="pdf")

submit1 = st.button("Tell me about my resume")
submit2 = st.button("How can I improve?")
submit3 = st.button("Missing keywords?")
submit4 = st.button("Percentage Match to job description")


if submit1:
    if uploaded_file is not None:
        pdf_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(jd, pdf_text, analyze_prompt)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        print("Please upload your resume!")

if submit2:
    if uploaded_file is not None:
        pdf_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(jd, pdf_text, improvement_prompt)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        print("Please upload your resume!")

if submit3:
    if uploaded_file is not None:
        pdf_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(jd, pdf_text, keyword_prompt)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        print("Please upload your resume!")

if submit4:
    if uploaded_file is not None:
        pdf_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(jd, pdf_text, percentage_prompt)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        print("Please upload your resume!")