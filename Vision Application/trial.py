from dotenv import load_dotenv
load_dotenv()
import os

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(prompt):
    response = model.generate_content(contents=prompt)
    return response.text

print(get_gemini_response("What kind of person are you?"))