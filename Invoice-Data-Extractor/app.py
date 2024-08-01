from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import time


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(upload_file):
    if upload_file is not None:
        # Read the file into bytes
        bytes_data = upload_file.getvalue()
        
        image_parts = [
            {
                "mime_type": upload_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

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

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)


submit = st.button("Extract Invoice Data")

input_prompt = """
You are an expert in reading invoices. 
The user has uploaded an invoice image and is asking for help.
If the user asks any questions about the invioce, read from the image and 
provide an answer.
"""

# When submit is clicked
if submit:
    with st.spinner('Generating response...'):
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input_text)
    st.header("The response to your question is: ")
    stream_response(response)