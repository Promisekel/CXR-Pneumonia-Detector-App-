from fastai.vision.all import PILImage

def predict(model, img_path):
    img = PILImage.create(img_path)
    pred_class, pred_idx, probs = model.predict(img)
    return pred_class


# Check if the image is an X-ray and classify for pneumonia
def is_xray(model, img_path):
    img = PILImage.create(img_path)
    pred_class, pred_idx, probs = model.predict(img)
    color = "green" if label == "PNEUMONIA" else "red"
    st.markdown(f"<p style='color:{color}; font-size:20px;'>Outcome of scan: {label}</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color:red; font-size:20px;'>X-RAY SCAN NOT WELL TAKEN. PLEASE SELECT ANOTHER ID.</p>", unsafe_allow_html=True)
  
    return pred_class in xray_classes
