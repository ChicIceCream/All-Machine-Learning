from dotenv import load_dotenv
load_dotenv()

import os
import PyPDF2 as pdf
import google.generativeai as genai

# Configure the Generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(resume_text, prompt):

    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Calling the model
    response = model.generate_content([resume_text, prompt])
    
    return response.text

def input_pdf_text(file_path):
    with open(file_path, "rb") as file:
        reader = pdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def main():    

    pdf_path = "C:\\Users\\User\\Downloads\\SJS Transcript Call.pdf"  # Replace with your file path
    if not os.path.exists(pdf_path):
        print("File not found!")
        return
    
    pdf_text = input_pdf_text(pdf_path)

    # Prompt for the model
    input_prompt = """
You are an expert in analyzing documents for investment insights. 
The user has uploaded a PDF containing information about a company's business.
Summarize this document with a focus on key elements that would interest an investor, including:

- Future growth prospects
- Notable changes in the business or strategy
- Potential key triggers for growth or risk
- Important details that could have a material impact on earnings and growth in the coming year

Please provide the summary in 3 concise paragraphs or fewer, highlighting only the most relevant insights for an investor.
"""


    print("Generating response...")
    response = get_gemini_response(input_prompt, pdf_text)
    print("The response to your question is: ")
    print(response)

if __name__ == "__main__":
    main()
