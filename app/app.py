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
import pathlib
##firebase
import firebase_admin
from firebase_admin import credentials, storage
from io import BytesIO

# Set the page title
st.set_page_config(page_title="CLAARITY PROJECT CXR PNEUMONIA DETECTOR")

# Add GitHub link with logo at the top
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <h3><a href="https://kccr-ghana.org/" target="_blank">
            <img src="https://drive.google.com/uc?export=view&id=1YcIOtPFb-VAYRpr5nKuoiK2tiAwlKmMl" alt="KCCR" style="margin: 10px;">
        </a>
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

# Temporary redirect PosixPath to WindowsPath
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Function to load models
@st.cache(allow_output_mutation=True)
def load_models():
    model = load_model()  # Load pneumonia prediction model
    xray_detector = load_xray_detector()  # Load X-ray detector model
    return model, xray_detector

st.title("CLAARITY PROJECT CXR PNEUMONIA DETERCTOR")
st.write("UPLOAD THE CHEST X-RAY TO PREDICT PATIENT PNEUMONIA OUTCOME.")

# Load models
model, xray_detector = load_models()

# Function to predict and display results
def predict_and_display_results(image):
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Checking if the image is an X-ray...")

    # Save uploaded image temporarily
    img_path = f"data/{uploaded_file.name}"
    image.save(img_path)

    if is_xray(xray_detector, img_path):
        st.write("Image is an X-ray. Classifying for pneumonia...")
        label = predict(model, img_path)
        st.write(f"Prediction: {label}")
    else:
        st.write("Uploaded image is not an X-ray. Please upload a chest X-ray image.")

# Handle file upload
#uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
######################################################################################
##################################################################################

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        predict_and_display_results(image)
    except:
        st.write("Invalid image file. Please try again.")

# Restore PosixPath after prediction
pathlib.PosixPath = temp
