from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st 
from PyPDF2 import PdfReader
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("")

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    os.makedirs("faiss_index", exist_ok=True)
    vector_store.save_local("faiss_index")
    print("FAISS index saved successfully.")

def get_conversational_chain():
    prompt_template = """
    Answer the question in as much detail as possible from the provided context. Make sure to provide all the 
    details. If the answer is not found to be in the provided context, give a generic output such as : "Answer is
    not available in the PDF", and make sure not to provide the wrong answer.
    Context : \n {context}? \n
    Question : \n {question} \n
    
    Answer : 
    """
    
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    if not os.path.exists("faiss_index/index.faiss"):
        print("FAISS index file not found. Please ensure the index has been created.")
        st.error("FAISS index file not found. Please ensure the index has been created.")
        return
    
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    
    chain = get_conversational_chain()
    
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    
    print(response)
    st.write(f'Reply: {response["output_text"]}')

def main():
    st.set_page_config("Chat With Multiple PDF") 
    st.header("Chat with Multiple PDF using Gemini 🤖") 
    
    user_question = st.text_input("Ask a Question from the PDF Files") 
    
    if user_question: 
        user_input(user_question) 
    
    with st.sidebar: 
        st.title("Menu:") 
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process", accept_multiple_files=True, type=["pdf"]) 
        if st.button("Submit & Process"): 
            with st.spinner("Processing..."): 
                raw_text = get_pdf_text(pdf_docs) 
                text_chunks = get_text_chunks(raw_text) 
                get_vector_store(text_chunks)
                st.success("Done")

if __name__ == "__main__":
    main()