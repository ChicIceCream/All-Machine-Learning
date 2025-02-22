from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt])
    return response.text

prompt = input("Enter your prompt: ")
response = get_gemini_response(prompt)
print("Response from Gemini:", response)