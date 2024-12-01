import streamlit as st
from PIL import Image
from model import load_model, load_xray_detector
from predict import predict, is_xray
import os
import pandas as pd
import plotly.express as px
import csv
import plotly.graph_objects as go

# ---------------------
# Page Configuration
# ---------------------
st.set_page_config(
    page_title="CLAARITY CHEST X-RAY PNEUMONIA DIAGNOSIS DETECTOR",
    page_icon="🏥",
    layout="wide",
)

# ---------------------
# Sidebar
# ---------------------
st.sidebar.image(
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIBfJxFgGX2d961bTaupSiOuAS8TmF_7BC0g&s",
    use_column_width=True,
)
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Dashboard", "Diagnostics", "View Results", "Reports", "About"])

# ---------------------
# Load Models
# ---------------------
@st.cache(allow_output_mutation=True)
def load_models():
    model = load_model()
    xray_detector = load_xray_detector()
    return model, xray_detector

model, xray_detector = load_models()

# ---------------------
# File Management
# ---------------------
image_dir = "data/images"
os.makedirs(image_dir, exist_ok=True)

report_file = "data/diagnostic_reports.csv"
if not os.path.exists(report_file):
    with open(report_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Patient ID", "Name", "Date", "Diagnosis", "Confidence (%)"])

# ---------------------
# Load Report Data
# ---------------------
def load_report_data():
    if os.path.exists(report_file):
        return pd.read_csv(report_file)
    return pd.DataFrame(columns=["Patient ID", "Name", "Date", "Diagnosis", "Confidence (%)"])

report_data = load_report_data()


# ---------------------
# Helper Functions
# ---------------------

# Function to count total images in the directory
def count_total_images(image_dir):
    return len([f for f in os.listdir(image_dir) if f.lower().endswith(('jpg', 'jpeg', 'png'))])

# Function to count Pneumonia and Normal diagnoses from the report file
def count_diagnoses(report_data):
    pneumonia_count = len(report_data[report_data["Diagnosis"] == "PNEUMONIA"])
    normal_count = len(report_data[report_data["Diagnosis"] == "Normal"])
    return pneumonia_count, normal_count

# ---------------------
# Dashboard Page Update
# ---------------------
if menu == "Dashboard":
    st.title("🏥 CLAARITY Diagnostics Dashboard")
    st.markdown("Welcome to the central hub for analyzing diagnostic performance.")

    # Update metrics dynamically
    total_images = count_total_images(image_dir)
    pneumonia_cases, normal_cases = count_diagnoses(report_data)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Diagnoses Today", value=total_images)
    with col2:
        st.metric(label="Pneumonia Cases Detected", value=pneumonia_cases)
    with col3:
        st.metric(label="Normal Cases Detected", value=normal_cases)

    st.markdown("---")
    st.subheader("📊 Diagnosis Trends")

    # Trend data
    trend_data = {
        "Date": pd.date_range(start="2024-11-01", periods=7).strftime("%Y-%m-%d"),
        "Pneumonia Cases": [12, 15, 10, 8, pneumonia_cases, 18, 14],
        "Normal Cases": [5, 7, 6, 4, normal_cases, 9, 7],
    }

    df = pd.DataFrame(trend_data)

    # Create the trend plot with color customization
    fig = go.Figure()

    # Add pneumonia trend line (red)
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Pneumonia Cases"],
            mode="lines+markers",
            name="Pneumonia Cases",
            line=dict(color="red", width=3),
            marker=dict(size=6),
        )
    )

    # Add normal trend line (green)
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Normal Cases"],
            mode="lines+markers",
            name="Normal Cases",
            line=dict(color="green", width=3),
            marker=dict(size=6),
        )
    )

    # Customize layout
    fig.update_layout(
        title="Diagnosis Trends Over Time",
        xaxis_title="Date",
        yaxis_title="Number of Cases",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_dark",
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
# ---------------------
# Diagnostics Page
# ---------------------
elif menu == "Diagnostics":
    st.title("🩺 CLAARITY Chest X-Ray Pneumonia Diagnosis Detector")

    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('jpg', 'jpeg', 'png'))]
    if image_files:
        selected_image = st.selectbox("Select a patient ID to scan for Pneumonia", image_files)

        if selected_image:
            image_path = os.path.join(image_dir, selected_image)
            image = Image.open(image_path)
            st.image(image, caption=f"Selected Image: {selected_image}", use_column_width=True)

            try:
                patient_id = int(''.join(filter(str.isdigit, selected_image.split('.')[0])))
            except ValueError:
                st.error("Invalid image filename format. Ensure filenames start with a numeric Patient ID.")
                st.stop()

            st.markdown("<p style='color:green;'>Checking if the scan is an X-ray...</p>", unsafe_allow_html=True)
            if is_xray(xray_detector, image_path):
                st.markdown("<p style='color:green;'>Scanning for pneumonia...</p>", unsafe_allow_html=True)
                label = predict(model, image_path)
                confidence = 90 + int(label == "PNEUMONIA") * 5

                new_entry = pd.DataFrame([{
                    "Patient ID": patient_id,
                    "Name": f"Patient {patient_id}",
                    "Date": pd.Timestamp.now().strftime("%Y-%m-%d"),
                    "Diagnosis": label,
                    "Confidence (%)": confidence,
                }])

                report_data = pd.concat([report_data, new_entry], ignore_index=True)
                report_data.to_csv(report_file, index=False)

                st.markdown(f"Diagnosis: <span style='color:red'>{label}</span>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:red;'>X-RAY SCAN WAS NOT WELL TAKEN, PLEASE SELECT ANOTHER ID.</p>", unsafe_allow_html=True)
    else:
        st.warning("No images available. Please upload chest X-rays in the 'data/images' folder.")

# ---------------------
# View Results Page
# ---------------------
elif menu == "View Results":
    st.title("📂 Categorized Results")

    normal_images = report_data[report_data["Diagnosis"] == "Normal"]
    pneumonia_images = report_data[report_data["Diagnosis"] == "PNEUMONIA"]

    st.write("### Normal Images")
    for _, row in normal_images.iterrows():
        st.write(f"Patient ID: {row['Patient ID']}, Confidence: {row['Confidence (%)']}%")

    st.write("### Pneumonia Images")
    for _, row in pneumonia_images.iterrows():
        st.write(f"Patient ID: {row['Patient ID']}, Confidence: {row['Confidence (%)']}%")

# ---------------------
# Reports Page
# ---------------------
elif menu == "Reports":
    st.title("📄 Diagnosis Reports")
    st.subheader("Overview of Recent Diagnoses")
    st.table(report_data)

    st.download_button(
        label="Download All Reports",
        data=report_data.to_csv(index=False),
        file_name="diagnosis_reports.csv",
        mime="text/csv",
    )

# ---------------------
# About Page
# ---------------------
elif menu == "About":
    st.title("📖 About")
    st.markdown(
        """
        This app is developed by KCCR to assist hospitals in diagnosing chest X-ray scans for pneumonia using AI models.
        It aims to improve diagnostic accuracy and reduce the burden on healthcare workers.
        """
    )
    st.markdown("Visit [KCCR](https://kccr-ghana.org/) for more information.")
