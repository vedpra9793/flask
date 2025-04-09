from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import io
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-1.5-pro")  # <-- Updated model
# model = genai.GenerativeModel("models/gemini-pro-vision")
# model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")


def gemini_response(input, image):
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(["Describe this image", image])
    return response.text

st.set_page_config(page_title="Gemini image demo")
st.header("Gemini Q&A demo")
input = st.text_input("Input: ", key="input")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(io.BytesIO(uploaded_file.read()))
    st.image(image, caption="Uploaded Image", use_column_width=True)



submit = st.button("tell me about this image") 
if submit:
    if uploaded_file is not None:
        response = gemini_response(input, image)
        st.subheader("Response:")
        st.write(response)
    else:
        st.warning("Please upload an image.")