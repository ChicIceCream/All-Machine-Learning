from dotenv import load_dotenv
load_dotenv()

from google import generativeai as genai
import streamlit as st
import os
import PyPDF2 as pdf

# configure my api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# define my function to call the api

def get_gemini_response(input, prompt):
    # Define my model here as flash model 
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # calling my model
    response = model.generate_content([input, prompt])
    
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    page = reader.pages[0]
    
    return page.extract_text()