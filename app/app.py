
# import streamlit as st
# from PIL import Image
# from model import load_model
# from predict import predict
# import pathlib


# # Temporary redirect PosixPath to WindowsPath
# temp = pathlib.PosixPath
# pathlib.PosixPath = pathlib.WindowsPath

# st.title("Pneumonia Detection from Chest X-rays")
# st.write("Upload a chest X-ray image to get a prediction.")

# model = load_model()

# # Restore PosixPath
# pathlib.PosixPath = temp

# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:

#     # Temporary redirect PosixPath to WindowsPath again during prediction
#     pathlib.PosixPath = pathlib.WindowsPath

#     image = Image.open(uploaded_file)
#     st.image(image, caption='Uploaded Image.', use_column_width=True)
#     st.write("")
#     st.write("Classifying...")

#     img_path = f"data/{uploaded_file.name}"
#     image.save(img_path)

#     # Restore PosixPath after prediction
#     pathlib.PosixPath = temp
    
#     label = predict(model, img_path)
#     st.write(f"Prediction: {label}")



import streamlit as st
from PIL import Image
from model import load_model, load_xray_detector
from predict import predict, is_xray
import os

# Set the page title
st.set_page_config(page_title="CLAARITY CHEST X-RAY PNEUMONIA DIAGNOSIS DETECTOR")

# GitHub link with logo at the top
import streamlit as st

st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <h3>
            <a href="https://kccr-ghana.org/" target="_blank">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIBfJxFgGX2d961bTaupSiOuAS8TmF_7BC0g&s" 
                     alt="Custom Icon" style="margin-right: 10px; width: 50px; height: auto;">
                KCCR
            </a>
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)


# Load models function
@st.cache(allow_output_mutation=True)
def load_models():
    model = load_model()
    xray_detector = load_xray_detector()
    return model, xray_detector

st.title("CLAARITY CHEST X-RAY PNEUMONIA DIAGNOSIS DETECTOR")
#st.write("Select a patient ID in the dropdown to Predict Pneumonia.")

# Load models
model, xray_detector = load_models()

# Directory where images are stored
image_dir = "data/images"
os.makedirs(image_dir, exist_ok=True)

# List images in the directory
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('jpg', 'jpeg', 'png'))]

# Display dropdown if images are available
if image_files:
    selected_image = st.selectbox("Select a patient ID in the dropdown to scan for Pneumonia", image_files)

if selected_image:
    image_path = os.path.join(image_dir, selected_image)
    
    # Display the image
    image = Image.open(image_path)
    st.image(image, caption=f"Selected Image: {selected_image}", use_column_width=True)
    st.write("Checking if the scan is an X-ray...")

    # Check if the image is an X-ray and classify for pneumonia
    if is_xray(xray_detector, image_path):
        st.write("Scanning for pneumonia...")
        label = predict(model, image_path) 
        st.write(f"Outcome of scan {"("selected_image")"}: {label}")
    else:
        st.write("X-RAY SCAN NOT WELL TAKEN. PLEASE SELECT ANOTHER ID.")
