import streamlit as st
from PIL import Image
from model import load_model, load_xray_detector
from predict import predict, is_xray
import os
import pandas as pd
import plotly.express as px

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
menu = st.sidebar.radio("Go to", ["Dashboard", "Diagnostics", "Reports", "About"])

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
# Dashboard Page
# ---------------------
if menu == "Dashboard":
    st.title("🏥 CLAARITY Diagnostics Dashboard")
    st.markdown("Welcome to the central hub for analyzing diagnostic performance.")

    # Example stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Diagnoses Today", value=42, delta="+5")
    with col2:
        st.metric(label="Pneumonia Cases Detected", value=30, delta="+3")
    with col3:
        st.metric(label="Other Diagnoses", value=12, delta="-2")

    st.markdown("---")
    st.subheader("📊 Diagnosis Trends")

    # Mock data for analytics
    data = pd.DataFrame({
        "Date": pd.date_range(start="2024-11-01", periods=7),
        "Pneumonia Cases": [12, 15, 10, 8, 20, 18, 14],
        "Other Cases": [5, 7, 6, 4, 8, 9, 7],
    })
    fig = px.line(
        data,
        x="Date",
        y=["Pneumonia Cases", "Other Cases"],
        labels={"value": "Cases", "variable": "Condition"},
        title="Diagnosis Trends Over Time",
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------
# Diagnostics Page
# ---------------------
elif menu == "Diagnostics":
    st.title("🩺 CLAARITY Chest X-Ray Pneumonia Diagnosis Detector")

    # Directory where images are stored
    image_dir = "data/images"
    os.makedirs(image_dir, exist_ok=True)

    # List images in the directory
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('jpg', 'jpeg', 'png'))]

    # Display dropdown if images are available
    if image_files:
        selected_image = st.selectbox("Select a patient ID to scan for Pneumonia", image_files)

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

                if label == "PNEUMONIA":
                    st.markdown(
                        f"Outcome of scan: (<span style='color:yellow'>{selected_image}</span>): <span style='color:red'>{label}</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"Outcome of scan: (<span style='color:yellow'>{selected_image}</span>): <span style='color:green'>{label}</span>",
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown("<p style='color:red;'>X-RAY SCAN WAS NOT WELL TAKEN, PLEASE SELECT ANOTHER ID.</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:red;'>NO IMAGE FOUND PLEASE REFRESH PAGE.</p>", unsafe_allow_html=True)
    else:
        st.warning("No images available. Please upload chest X-rays in the 'data/images' folder.")

# ---------------------
# Reports Page
# ---------------------
elif menu == "Reports":
    st.title("📄 Diagnosis Reports")

    # Mock data for reports
    report_data = pd.DataFrame({
        "Patient ID": [101, 102, 103, 104],
        "Name": ["Alice", "Bob", "Charlie", "Diana"],
        "Date": ["2024-11-01", "2024-11-02", "2024-11-03", "2024-11-04"],
        "Diagnosis": ["Pneumonia", "Normal", "TB", "Pneumonia"],
        "Confidence (%)": [92, 89, 95, 94],
    })
    st.subheader("Overview of Recent Diagnoses")
    st.table(report_data)

    # Download button for reports
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
