import os
from io import BytesIO

import requests
import streamlit as st
from PIL import Image


def check_api_health(api_url: str) -> bool:
    """Check if the api is up and running"""
    try:
        response = requests.get(f"{api_url}/health")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


api_url = os.getenv("API_URL", "http://localhost:8000/api")

is_api_up = check_api_health(api_url)

if is_api_up is True:
    st.title("MobileSam Segmentation Model Service")
    st.write("Upload an image to segment")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        try:
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(f"{api_url}/segment-image", files=files)

            if response.status_code == 200:
                segmented_image = Image.open(BytesIO(response.content))
                st.image(
                    segmented_image, caption="Segmented Image", use_column_width=True
                )
            else:
                st.error("Failed to segment the provided image")
        except Exception:
            st.error("Failed to send request")

else:
    st.error("API is down!")
