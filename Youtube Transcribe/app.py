import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import pathlib
import os

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

prompt = """
You are an expert Youtube summarizer. You will be taking the transcript text and summarizing the entire video
and provide the most important summaryu in points all within 250 words. Make it as informative as you can and 
should give as much context from the transcript as you can. Here is the transcript text : 
"""

def get_gemini_response(prompt, transcript):
    model = genai.GenerativeModel("gemini-pro")
    
    response = model.generate_content(prompt + transcript)
    
    if response and response.parts:
        return response.parts[0].text
    else:
        return "No response received."


def extract_details(url):
    try:
        video_id = url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id=video_id)
        transcript = ""
        
        for i in transcript_text:
            if len(transcript) < 1000:
                transcript += " " + i["text"]
            
        return transcript
                
    except Exception as e:
        raise e

st.title("YouTube Video Summarizer")

url = st.text_input("Enter YouTube URL:")

if url:
    video_id = url.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg")

if st.button("Summarize"):
    if url:
        with st.spinner("Extracting transcript..."):
            try:
                transcript = extract_details(url)
                with st.spinner("Generating summary..."):
                    summary = get_gemini_response(prompt, transcript)
                    st.write("### Summary")
                    st.write(summary)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("Please enter a valid YouTube URL.")