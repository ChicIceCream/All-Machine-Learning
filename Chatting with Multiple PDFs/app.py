from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st 
from PyPDF2 import PdfReader
import google.generativeai as genai

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("")

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extractText
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap = 1000)
    chunks = text_splitter.split_text(text)
    
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question in as much detail as possible from the provided context. Make sure to provide all the 
    details. If the answer is not found to be in the provided context, give a generic output such as : "Answer is
    not available in the PDF", and make sure not to provide the wrong answer
    Context : \n {context}? \n
    Question : \n {question} \n
    
    Answer : 
    """
    
    model = ChatGoogleGenerativeAI(model = "gemini-pro")