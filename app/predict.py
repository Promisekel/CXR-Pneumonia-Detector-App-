from fastai.vision.all import PILImage

def predict(model, img_path):
    img = PILImage.create(img_path)
    pred_class, pred_idx, probs = model.predict(img)
    return pred_class


def is_xray(model, img_path):
    img = PILImage.create(img_path)
    pred_class, pred_idx, probs = model.predict(img)
    # Check if the predicted class is in the Xray classes
    predicted_class = "PNEUMONIA"  # or "NORMAL"
    xray_classes = ["PNEUMONIA", "NORMAL"]
    if predicted_class in xray_classes:
    if predicted_class == "PNEUMONIA":
        # Display text in red for pneumonia
        st.markdown(f"<h3 style='color:red;'>{predicted_class}</h3>", unsafe_allow_html=True)
    else:
        # Display text in green for normal
        st.markdown(f"<h3 style='color:green;'>{predicted_class}</h3>", unsafe_allow_html=True)

    return pred_class in xray_classes
