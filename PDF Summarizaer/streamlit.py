from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai
import time

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

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

# Function to display text in a streaming manner by chunks
def stream_response(response_text, chunk_size=14):
    placeholder = st.empty()
    words = response_text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    text = ""
    for chunk in chunks:
        for letter in chunk:
            text += letter
            placeholder.text(text)
            time.sleep(0.01)  # Adjust the speed of letter streaming here
        text += "\n\n"
        placeholder.text(text)
        time.sleep(0.5)  # Adjust the speed of chunk streaming here

## Initialising Streamlit application
st.set_page_config(page_title="Invoice Data Extractor")
st.title("Invoice Data Extractor")

input_text = st.text_input("Input: ", key="input")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
pdf_text = None
if uploaded_file is not None:
    pdf_text = input_pdf_text(uploaded_file)


submit = st.button("Extract Invoice Data")

input_prompt = """
You are an expert in reading pdfs. 
The user has uploaded a pdf for you to summarise. give the sumamry of the input data    
"""

# When submit is clicked
if submit:
    with st.spinner('Generating response...'):
        pdf_data = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt, pdf_data, input_text)
    st.header("The response to your question is: ")
    stream_response(response)
    print(response)