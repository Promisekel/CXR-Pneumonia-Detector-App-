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
import firebase_admin
from firebase_admin import credentials, storage
from io import BytesIO

# Initialize Firebase Admin SDK
cred = credentials.Certificate("app/your-firebase-credentials.json")  # Replace with your Firebase credentials JSON path
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-firebase-bucket-name.appspot.com'  # Replace with your Firebase Storage bucket name
})

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

# Function to load models
@st.cache(allow_output_mutation=True)
def load_models():
    model = load_model()  # Load pneumonia prediction model
    xray_detector = load_xray_detector()  # Load X-ray detector model
    return model, xray_detector

st.title("CLAARITY PROJECT CXR PNEUMONIA DETECTOR")
st.write("UPLOAD THE CHEST X-RAY TO PREDICT PATIENT PNEUMONIA OUTCOME.")

# Load models
model, xray_detector = load_models()

# Function to upload image to Firebase Storage
def upload_image_to_firebase(image, file_name):
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_file(image, content_type="image/jpeg")
    # Make the file publicly accessible if needed
    blob.make_public()
    return blob.public_url

# Function to predict and display results
def predict_and_display_results(image, file_url):
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Checking if the image is an X-ray...")

    if is_xray(xray_detector, file_url):
        st.write("Image is an X-ray. Classifying for pneumonia...")
        label = predict(model, file_url)
        st.write(f"Prediction: {label}")
    else:
        st.write("Uploaded image is not an X-ray. Please upload a chest X-ray image.")

# Handle file upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        # Convert image to BytesIO for upload
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        # Upload to Firebase and get the public URL
        file_url = upload_image_to_firebase(image_io, uploaded_file.name)
        
        # Predict and display results
        predict_and_display_results(image, file_url)
    except Exception as e:
        st.write("An error occurred while processing the image.")
        st.write(f"Error: {e}")
