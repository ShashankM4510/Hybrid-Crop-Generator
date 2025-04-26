import streamlit as st
import requests
import base64
from PIL import Image
import io
import os

# HuggingFace API settings
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
HF_TOKEN = st.secrets["HF_TOKEN"]  # From secrets.toml

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None

def generate_hybrid(crop1, crop2):
    prompt = f"A realistic hybrid plant combining {crop1} and {crop2}, highly detailed, 4K, professional photo, realistic farm background"
    with st.spinner('Generating your hybrid crop...'):
        output = query({"inputs": prompt})
    return output

# Streamlit App
st.set_page_config(page_title="Hybrid Crop Generator", page_icon="🌾")
st.title("🌾 Hybrid Crop Image Generator using AI 🚀")
st.write("Upload two crop images and generate a hybrid crop!")

uploaded_file1 = st.file_uploader("Upload First Crop Image", type=["jpg", "jpeg", "png"])
uploaded_file2 = st.file_uploader("Upload Second Crop Image", type=["jpg", "jpeg", "png"])

if uploaded_file1 and uploaded_file2:
    col1, col2 = st.columns(2)
    with col1:
        crop1_name = st.text_input("Name of First Crop (e.g., Tomato)", key="crop1")
        st.image(uploaded_file1, caption="First Crop", use_column_width=True)
    with col2:
        crop2_name = st.text_input("Name of Second Crop (e.g., Potato)", key="crop2")
        st.image(uploaded_file2, caption="Second Crop", use_column_width=True)

    if st.button("Generate Hybrid Crop", type="primary"):
        if crop1_name and crop2_name:
            hybrid_image_bytes = generate_hybrid(crop1_name, crop2_name)
            
            if hybrid_image_bytes:
                try:
                    hybrid_image = Image.open(io.BytesIO(hybrid_image_bytes))
                    st.success("Hybrid crop generated successfully!")
                    st.image(hybrid_image, 
                            caption=f"🌟 Hybrid: {crop1_name} + {crop2_name}", 
                            use_column_width=True)
                    
                    # Download button
                    buf = io.BytesIO()
                    hybrid_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    st.download_button(
                        label="Download Hybrid Image",
                        data=byte_im,
                        file_name=f"hybrid_{crop1_name}_{crop2_name}.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Failed to process image: {str(e)}")
            else:
                st.warning("Image generation failed. Please try again.")
        else:
            st.warning("Please enter names for both crops!")