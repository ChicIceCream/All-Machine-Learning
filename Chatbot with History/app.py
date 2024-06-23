from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load gemini pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit application
st.set_page_config(page_title="Chatbot with History")

st.header("Gemini Chatbot with History")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Get user input
input_text = st.text_input("Input: ", key="input")
submit = st.button("Submit")

if submit and input_text:
    response = get_gemini_response(input_text)
    
    # Append the input and response to the chat history
    st.session_state['chat_history'].append(("You", input_text))
    st.subheader("The response is: ")
    
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Gemini", chunk.text))

# Display chat history
st.subheader("The chat history is: ")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
