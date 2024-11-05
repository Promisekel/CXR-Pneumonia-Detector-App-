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
cred = credentials.Certificate("path/to/your/firebase_credentials.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-firebase-storage-bucket-name.appspot.com'
})

# Function to list files in a Firebase Storage directory
def list_files_in_directory(directory_path):
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix=directory_path)
    file_paths = [blob.name for blob in blobs if blob.name != directory_path]  # Exclude the directory itself
    return file_paths

# Function to download an image file from Firebase Storage
def download_image_from_firebase(file_path):
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    image_data = blob.download_as_bytes()
    return image_data

# Streamlit UI
st.title("Select and Display Image from Firebase Storage")

# List files in the directory
directory_path = "your-directory-path/"  # Replace with your Firebase directory
file_paths = list_files_in_directory(directory_path)

# Allow user to select a file
selected_file = st.selectbox("Select an image to display", file_paths)

# Download and display the selected image
if selected_file:
    try:
        image_data = download_image_from_firebase(selected_file)
        image = Image.open(BytesIO(image_data))
        st.image(image, caption=f"Displaying: {selected_file}", use_column_width=True)
    except Exception as e:
        st.write("Failed to download the image from Firebase Storage.")
        st.write(e)
##################################################################################

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        predict_and_display_results(image)
    except:
        st.write("Invalid image file. Please try again.")

# Restore PosixPath after prediction
pathlib.PosixPath = temp
