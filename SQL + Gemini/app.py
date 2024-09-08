from dotenv import load_dotenv
load_dotenv() # loading all env data

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

## Configure our API Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load my Google GEN model and provide sql as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    
    return response.text

## Function to retrieve query from sql database 
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    
    return rows

## Define my prompt
prompt =[
    '''
    You are an expert in transforming natural language into SQL queries that interact with a database.
    Please analyze the user-provided question, understand the context of the data structure, and generate an efficient SQL query.
    Ensure that the query is optimized for performance, avoids redundancy, and includes any necessary joins or conditions to fetch the relevant data.
    The database tables have columns related to [provide context about the tables and their key columns].
    
    User question: "Get the names of all students who scored more than 80 marks."
    SQL query:
    SELECT NAME FROM STUDENT WHERE MARKS > 80;

    User question: "Find the students in Class 10, Section A."
    SQL query:
    SELECT * FROM STUDENT WHERE CLASS = '10' AND SECTION = 'A';

    User question: "Show the total marks for students in Class 9."
    SQL query:
    SELECT SUM(MARKS) FROM STUDENT WHERE CLASS = '9';

    User question: "List all students in Section B, ordered by their marks."
    SQL query:
    SELECT NAME, MARKS FROM STUDENT WHERE SECTION = 'B' ORDER BY MARKS DESC;

    also the sql code should not have ``` in the beginning or end and sql word in output
    '''
]

## Streamlit App
st.set_page_config(page_title="l can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")
question=st.text_input("Input : ", key="input")

submit=st.button("Ask the question: ")

# if submit is clicked

if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    
    data = read_sql_query(response, "student.db")
    
    st.subheader("The response is :")
    for row in data:
        print(row)
        st.header(row)
