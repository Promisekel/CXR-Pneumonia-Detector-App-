import streamlit as st
from PIL import Image
from model import load_model, load_xray_detector
from predict import predict, is_xray
import os
import pandas as pd
import plotly.express as px
import csv
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    use_container_width=True,
)
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Dashboard", "Diagnostics","Reports", "About"]) #"View Results", 

# ---------------------
# Load Models
# ---------------------
@st.cache_resource
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
    st.subheader("📊 Diagnosis Trends and Summary")

    # Prepare trend data from the report
    report_data["Date"] = pd.to_datetime(report_data["Date"])  # Ensure proper date format
    report_data_grouped = report_data.groupby("Date")["Diagnosis"].value_counts().unstack(fill_value=0)
    report_data_grouped = report_data_grouped.rename(columns={"PNEUMONIA": "Pneumonia Cases", "Normal": "Normal Cases"}).reset_index()

    # Ensure the dataframe has values for plotting
    if "Pneumonia Cases" not in report_data_grouped.columns:
        report_data_grouped["Pneumonia Cases"] = 0
    if "Normal Cases" not in report_data_grouped.columns:
        report_data_grouped["Normal Cases"] = 0

    # Create subplot layout: 2 rows, 1 column
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.1,
        subplot_titles=("Diagnosis Trend Over Time", "Diagnosis Bar Chart"),
        row_heights=[0.7, 0.3]  # Adjust row heights
    )

    # Add line trace for pneumonia cases (red)
  #  fig.add_trace(
   #     go.Scatter(
   #         x=report_data_grouped["Date"],
   #         y=report_data_grouped["Pneumonia Cases"],
   #         mode="lines+markers",
    #        name="Pneumonia Cases",
    #        line=dict(color="red", width=3),
    #        marker=dict(size=6),
   #     ),
   #     row=1, col=1  # Add to first row, first column
   # )

    # Add line trace for normal cases (green)
   # fig.add_trace(
   #    go.Scatter(
    #        x=report_data_grouped["Date"],
    #        y=report_data_grouped["Normal Cases"],
     #       mode="lines+markers",
     #       name="Normal Cases",
      #      line=dict(color="green", width=3),
      #      marker=dict(size=6),
    #    ),
    #    row=1, col=1  # Add to first row, first column
   # )

    # Add bar trace for pneumonia cases (red)
    fig.add_trace(
        go.Bar(
            x=report_data_grouped["Date"],
            y=report_data_grouped["Pneumonia Cases"],
            name="Pneumonia Cases (Bar)",
            marker_color="red",
            opacity=5,
        ),
        row=2, col=1  # Add to second row, first column
    )

    # Add bar trace for normal cases (green)
    fig.add_trace(
        go.Bar(
            x=report_data_grouped["Date"],
            y=report_data_grouped["Normal Cases"],
            name="Normal Cases (Bar)",
            marker_color="green",
            opacity=5,
        ),
        row=2, col=1  # Add to second row, first column
    )

    # Update layout to ensure clear axes and legend
    fig.update_layout(
        title="Diagnosis Trends and Bar Graph Summary",
        xaxis_title="Date",
        yaxis_title="Number of Cases",
        barmode="group",  # Group bars side by side
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_dark",
        showlegend=True,
        height=700,  # Adjust overall height for both plots
    )

    # Display the plots
    st.plotly_chart(fig, use_container_width=True)

# ---------------------
# Diagnostics Page
# ---------------------
elif menu == "Diagnostics":
    st.title("🩺 CLAARITY Chest X-Ray Pneumonia Diagnosis Detector")
    
    # Initialize session state for image selection if not already set
    if 'selected_patient_id' not in st.session_state:
        st.session_state.selected_patient_id = None
    
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('jpg', 'jpeg', 'png'))]

    if image_files:
        selected_image = st.selectbox("Select a patient ID to scan for Pneumonia", image_files, key="patient_id_selectbox")

        if selected_image:
            st.session_state.selected_patient_id = selected_image  # Save selected patient ID in session state
            image_path = os.path.join(image_dir, selected_image)
            image = Image.open(image_path)
            st.image(image, caption=f"Selected Image: {selected_image}", width=600) #use_column_width=True)

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
                st.session_state.selected_patient_id = None  # Reset the patient ID selection after prediction
            else:
                st.markdown("<p style='color:red;'>X-RAY SCAN WAS NOT WELL TAKEN, PLEASE SELECT ANOTHER ID.</p>", unsafe_allow_html=True)

    else:
        st.warning("No images available. Please upload chest X-rays in the 'data/images' folder.")

# ---------------------
# View Results Page
# ---------------------
#elif menu == "View Results":
#    st.title("📂 Categorized Results")

 #   normal_images = report_data[report_data["Diagnosis"] == "Normal"]
 #   pneumonia_images = report_data[report_data["Diagnosis"] == "PNEUMONIA"]

 #   st.write("### Normal Images")
 #   for _, row in normal_images.iterrows():
 #       st.write(f"Patient ID: {row['Patient ID']}, Confidence: {row['Confidence (%)']}%")

  #  st.write("### Pneumonia Images")
  #  for _, row in pneumonia_images.iterrows():
  #      st.write(f"Patient ID: {row['Patient ID']}, Confidence: {row['Confidence (%)']}%")

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
        This app is developed by KCCR to as part of the CLAARITY Project for diagnosing chest X-ray scans for pneumonia using AI models.
        It aims to improve diagnostic accuracy and reduce time.
        """
    )
    st.markdown("Visit [KCCR](https://kccr-ghana.org/) for more information.")

