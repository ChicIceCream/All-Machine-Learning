import base64
import io
from dotenv import load_dotenv
load_dotenv()

import streamlit as st 
import os
import google.generativeai as genai
import pdf2image


genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to Image      
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page = images[0]
        # Convert to  bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return  pdf_parts
    else:
        raise  FileNotFoundError("No  file  uploaded")

# Streamlit app :
st.set_page_config(page_title="ATS Resume Review")
st.header("ATS Tracking system")
input_text = st.text_area("Job Description: ", key='input')
uploaded_file = st.file_uploader("Upload your resume here (PDF): ", type=['pdf'])

submit1 = st.button("Tell me about my resume")
submit2 = st.button("How can I improve?")
submit3 = st.button("Missing keywords?")
submit4 = st.button("Percentage Match to job description")

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

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(analyze_prompt, pdf_content, input_text)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        print("Please upload your resume!")

if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(improvement_prompt, pdf_content, input_text)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        print("Please upload your resume!")

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(keyword_prompt, pdf_content, input_text)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        print("Please upload your resume!")

if submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(percentage_prompt, pdf_content, input_text)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        print("Please upload your resume!")
