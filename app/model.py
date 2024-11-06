from fastai.learner import load_learner
import pathlib
import platform

# Avoid overriding WindowsPath with PosixPath
# This may not be needed unless there's a specific reason, so it's omitted
# pathlib.WindowsPath = pathlib.PosixPath

def load_model():
    model_path = 'saved_model/pneumonia_classification_model.pkl'
    
    # Ensure the path is a string
    model_path_str = str(model_path)
    
    # Debugging: Print the path to ensure it's correct
    print(f"Loading model from: {model_path_str}")
    
    try:
        # Load the model
        model = load_learner(model_path_str)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def load_xray_detector():
    xray_model_path = 'saved_model/xray_detector_model.pkl'
    
    try:
        # Load the X-ray detector model
        xray_model = load_learner(xray_model_path)
        return xray_model
    except Exception as e:
        print(f"Error loading X-ray detector model: {e}")
        return None
