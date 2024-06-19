from dotenv import load_dotenv

load_dotenv() ## This will oad all the enviornment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
def get_gemini_response(question):
    '''
    This function will load the Gemini model and get responses
    '''
    
    response = model.generate_content(question)
    
    return response.text

## Now we will set up our Streamlit application

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

input = st.text_input("Input: ",key="input")
submit = st.button("Ask the question")

# When submit is clicked
if submit:
    response = get_gemini_response(input)
    st.header("The response to your question is : ")
    st.write(response)
