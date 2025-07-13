
import streamlit as st
import joblib
import pytesseract
from PIL import Image
import requests

st.set_page_config(page_title="Emotional Blackmail Detector", layout="centered")
st.title("🧠 Emotional Blackmail Detector")
st.write("Enter a message or upload a screenshot to detect emotional manipulation or support.")

input_method = st.radio("Choose Input Method", ["Text", "Image"])
api_url = "https://44846758d0a6.ngrok-free.app/"  # Update with your API

if input_method == "Text":
    user_input = st.text_area("Enter your message:")
    if st.button("Analyze Text"):
        if user_input.strip():
            try:
                response = requests.post(api_url, json={"text": user_input})
                if response.status_code == 200:
                    st.success(f"🧾 **Detected Emotion Type:** `{response.json()['prediction']}`")
                else:
                    st.error("Error: Unable to analyze text.")
            except Exception as e:
                st.error(f"Request failed: {e}")
        else:
            st.warning("Please enter a message.")
else:
    uploaded_image = st.file_uploader("Upload a chat screenshot", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        if st.button("Analyze Image Text"):
            try:
                extracted_text = pytesseract.image_to_string(image)
                if extracted_text.strip():
                    response = requests.post(api_url, json={"text": extracted_text})
                    if response.status_code == 200:
                        st.info(f"📜 Extracted Text: {extracted_text.strip()[:300]}...")
                        st.success(f"🧾 Detected Emotion Type: `{response.json()['prediction']}`")
                    else:
                        st.error("API returned an error.")
                else:
                    st.warning("No readable text found.")
            except Exception as e:
                st.error(f"OCR failed: {e}")
