from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import io
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Gemini image Q&A
def gemini_response(input_text, image):
    if input_text:
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(["Describe this image", image])
    return response.text

# Streamlit Page Config
st.set_page_config(page_title="Gemini Vision App", layout="centered")
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .title {
        text-align: center;
        font-size: 3em;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #2ecc71;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.5em;
    }
    .stButton>button:hover {
        background-color: #27ae60;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# UI
st.markdown("<div class='title'>🧠 Gemini Vision Q&A</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Upload an image and ask anything about it!</div>", unsafe_allow_html=True)

with st.container():
    input_text = st.text_input("Ask a question about the image (or leave blank to describe it):", key="input")

    uploaded_file = st.file_uploader("📷 Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(io.BytesIO(uploaded_file.read()))
        st.image(image, caption="Uploaded Image", use_column_width=True)

    submit = st.button("✨ Tell me about this image")

    if submit:
        if uploaded_file is not None:
            with st.spinner("Thinking... 🤔"):
                response = gemini_response(input_text, image)
            st.success("Here's what I found:")
            st.markdown(f"""<div style='background-color: #000000; color: #ffffff; padding: 1.2em; border-radius: 12px; font-size: 1.1em; line-height: 1.6;'>{response}</div>""",unsafe_allow_html=True
)

        else:
            st.warning("Please upload an image first.")
