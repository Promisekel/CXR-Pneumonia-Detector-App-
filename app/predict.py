from fastai.vision.all import PILImage

def predict(model, img_path):
    img = PILImage.create(img_path)
    pred_class, pred_idx, probs = model.predict(img)
    return pred_class


def is_xray(model, img_path):
    img = PILImage.create(img_path)
    pred_class, pred_idx, probs = model.predict(img)
    # Check if the predicted class is in the Xray classes
    xray_classes = ["PNEUMONIA", "NORMAL"]
   if pred_class in xray_classes:
        # Set color based on the prediction
        color = "green" if pred_class == "PNEUMONIA" else "red"
        # Display the outcome with the respective color
        st.markdown(f"<p style='color:{color}; font-size:20px;'>Outcome of scan: {pred_class}</p>", unsafe_allow_html=True)
 
  
    return pred_class in xray_classes
