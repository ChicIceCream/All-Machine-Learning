from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai
import streamlit as st
from PIL import Image
import time

genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

def get_gemini_response(prompt, image):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt, image])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "bytes_info": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("There does not seem to be any files submitted. Please re-check.")


prompt = """
You are a highly advanced AI model specialized in analyzing food images to estimate their calorie content. 
Given an image of a meal, provide a detailed breakdown of the food items present and their respective calorie counts.
If you cannot be accurate, or cannot decide how much calories can one serving provide, give an avergae calorie for that
dish that should be true for most. 

After recognising the food in the image, the output should be a list of the food and their calories. Only give an answer
like the example
Here is an example : 
1. Item 1 --- no. of calories
2. Item 2 --- no. of calories

List them one by one, do not put it into a single line
Finally, mention whether this food is healthy for an average person or not. In the end, write a short percentage
overview on the nutirents as a ratio in the food. For example : 
50% carbs, 30% protein. 

"""


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



## Initialise my streamlit app

st.header("Calories Advisor App")

uploaded_file = st.file_uploader("Enter an image of your meal!", type=["jpg", "png", "jpeg"])

image = None
if uploaded_file is not None:
    meal_image = Image.open(uploaded_file)  # Open image using PIL
    st.image(meal_image)  # Display the uploaded image in Streamlit
    image = meal_image  # Store the image for later use in the API call

# Button to trigger calorie check when pressed.
if st.button("Check for calories"):
    if image is not None:
        # Correct: passing `image` directly as a PIL image object to the API.
        response = get_gemini_response(prompt, image)
        st.header("The streamed response is: ")
        # st.write(stream_response(response))
        # st.write("More structured response : ")
        st.write(response)
    else:
        st.error("Please upload an image before checking for calories.")