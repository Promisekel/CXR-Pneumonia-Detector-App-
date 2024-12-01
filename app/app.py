import streamlit as st
from PIL import Image
from model import load_model, load_xray_detector
from predict import predict, is_xray
import pandas as pd
import os
import csv

# Set up page title
st.set_page_config(page_title="CLAARITY CHEST X-RAY PNEUMONIA DIAGNOSTIC DETECTOR")

# logo and description
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

# Load models
model, xray_detector = load_models()

# Directory where images are stored
image_dir = "data/images"
os.makedirs(image_dir, exist_ok=True)

# File for storing diagnostic reports
report_file = "data/diagnostic_reports.csv"
if not os.path.exists(report_file):
    # Initialize the report CSV if it doesn't exist
    with open(report_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Patient ID", "Name", "Date", "Diagnosis", "Confidence (%)"])

# Read existing reports
report_data = pd.read_csv(report_file)

# Display navigation
page = st.sidebar.radio("Navigate", ["Diagnosis", "View Results", "Reports"])

# Diagnosis page
if page == "Diagnosis":
    st.subheader("Select an image to diagnose pneumonia")

    # List images in the directory
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('jpg', 'jpeg', 'png'))]

    if image_files:
        selected_image = st.selectbox("Select a patient ID in the dropdown to scan for Pneumonia", image_files)

    if selected_image:
        image_path = os.path.join(image_dir, selected_image)
        
        # Display the image
        image = Image.open(image_path)
        st.image(image, caption=f"Selected Image: {selected_image}", use_column_width=True)

        st.markdown("<p style='color:green;'>Checking if the scan is an X-ray...</p>", unsafe_allow_html=True)

        # Check if the image is an X-ray and classify for pneumonia
        if is_xray(xray_detector, image_path):
            st.markdown("<p style='color:green;'>Scanning for pneumonia...</p>", unsafe_allow_html=True)
            label = predict(model, image_path)
            
            # Show the result
            confidence = 90 + int(label == "PNEUMONIA") * 5  # Mock confidence level
            st.markdown(f"Diagnosis: <span style='color:red'>{label}</span>", unsafe_allow_html=True)

            # Update diagnostic report
            patient_id = int(selected_image.split('.')[0])  # Extract ID from filename
            report_entry = {
                "Patient ID": patient_id,
                "Name": f"Patient {patient_id}",  # Mock name
                "Date": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "Diagnosis": label,
                "Confidence (%)": confidence,
            }
            report_data = report_data.append(report_entry, ignore_index=True)
            report_data.to_csv(report_file, index=False)
        else:
            st.markdown("<p style='color:red;'>X-RAY SCAN WAS NOT WELL TAKEN, PLEASE SELECT ANOTHER ID.</p>", unsafe_allow_html=True)

    else:
        st.markdown("<p style='color:red;'>NO IMAGE FOUND PLEASE REFRESH PAGE.</p>", unsafe_allow_html=True)

# View Results page
elif page == "View Results":
    st.subheader("View Diagnosed Results")

    # Categorized views (Normal/Pneumonia)
    normal_images = report_data[report_data["Diagnosis"] == "Normal"]
    pneumonia_images = report_data[report_data["Diagnosis"] == "PNEUMONIA"]

    # Display Normal images
    st.write("### Normal Images")
    for _, row in normal_images.iterrows():
        st.write(f"Patient ID: {row['Patient ID']}, Confidence: {row['Confidence (%)']}%")

    # Display Pneumonia images
    st.write("### Pneumonia Images")
    for _, row in pneumonia_images.iterrows():
        st.write(f"Patient ID: {row['Patient ID']}, Confidence: {row['Confidence (%)']}%")

# Reports page
elif page == "Reports":
    st.subheader("Overview of Recent Diagnoses")
    st.table(report_data)

    # Download button for reports
    st.download_button(
        label="Download All Reports",
        data=report_data.to_csv(index=False),
        file_name="diagnosis_reports.csv",
        mime="text/csv",
    )
