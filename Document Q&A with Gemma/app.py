import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS ##vector store db
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings ## vector embedding techniques

from dotenv import load_dotenv

load_dotenv()

# Load the Groq and Google API

groq_api_key = os.getenv("GROQ_API_KEY")
os.environ('GOOGLE_API_KEY') = os.getenv("GOOGLE_API_KEY")

st.title("Gemma Document Q&A")

llm = ChatGroq(
    groq_api_key = groq_api_key,
    model = "Gemma-7b-it"
)

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question.
    <context>
    {context}
    <context>
    Question:{input}
    """
)

def vector_embeddings():
    