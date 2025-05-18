# Q&A Chatbot
from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# ✅ Correct way to read the API key from environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the Gemini model and get response
def get_gemini_response(prompt_text, image, user_input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt_text, image[0], user_input])
    return response.text

# Function to handle uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app UI
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

user_input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

# Expert prompt
input_prompt = """
As a user, I should provide a path to the image, and the program should display the text from the
image. 
"""

# Generate and display response
if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, user_input)
        st.subheader("The Response is:")
        st.write(response)
    except Exception as e:
        st.error(f"Error: {e}")
