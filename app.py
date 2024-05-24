
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

css='./style.css'




def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

# Set the page configuration at the very beginning
st.set_page_config(page_title="AI Nutritionist")

# Function to inject custom CSS
def local_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom CSS
local_css("style.css")

# Streamlit app content inside a container
st.markdown('<div class="stApp">', unsafe_allow_html=True)

st.header("AI Nutritionist")
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the food.", type="primary")

# Closing the container div
st.markdown('</div>', unsafe_allow_html=True)

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
               Total calories:
               Overall Assessment:

            Overall Healthy: Yes/No 
            Suitable Age Groups: 

note: do not provide any vague answers apart from the topic and if some issue in recognizing the food item then raise a error or statement telling 
couldnt recognise a dish


"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input_text)
    st.subheader("The Response is")
    st.write(response)

