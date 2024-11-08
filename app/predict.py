from fastai.vision.all import PILImage
from PIL import Image as PILImage

def predict(model, img_path):
    img = PILImage.create(img_path)
    pred_class, pred_idx, probs = model.predict(img)
    return pred_class


def is_xray(model, img_path):
    img = PILImage.open(img_path)
    pred_class, pred_idx, probs = model.predict(img)
    
    # Define X-ray classes
    xray_classes = ["PNEUMONIA", "NORMAL"]
    
    # Check if the predicted class is in the X-ray classes
    if pred_class in xray_classes:
        # Determine color based on predicted class
        color = "red" if pred_class == "NORMAL" else "green"
        # Display the outcome with the respective color
        st.markdown(f"<p style='color:{color};'>Outcome of scan: {pred_class}</p>", unsafe_allow_html=True)
        
    return pred_class in xray_classes

