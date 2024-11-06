# Streamlit try
from fastai.learner import load_learner
import pathlib
import platform

#plt = platform.system()
#pathlib.WindowsPath = pathlib.PosixPath

#def load_model():
 #   model_path = 'saved_model/pneumonia_classification_model.pkl'
    
    # Ensure the path is a string
  #  model_path_str = str(model_path)
    
    # Debugging: Print the path to ensure it's correct
   # print(f"Loading model from: {model_path_str}")
    
    # Load the model
    #model = load_learner(model_path_str)
    
    # Return the model to you
    #return model

#def load_xray_detector():
 #   xray_model_path = 'saved_model/xray_detector_model.pkl'
  #  xray_model = load_learner(xray_model_path)
   # return xray_model

from fastai.learner import load_learner
import pathlib
import platform

# Ensure platform compatibility with Pathlib only on Windows
if platform.system() == 'Windows':
    pathlib.WindowsPath = pathlib.PosixPath

def load_model():
    model_path = 'saved_model/pneumonia_classification_model.pkl'
    model_path_str = str(model_path)  # Ensure model path is a string for load_learner
    print(f"Loading model from: {model_path_str}")  # Debugging statement
    model = load_learner(model_path_str)
    return model

def load_xray_detector():
    xray_model_path = 'saved_model/xray_detector_model.pkl'
    print(f"Loading X-ray detector model from: {xray_model_path}")
    xray_model = load_learner(xray_model_path)
    return xray_model
