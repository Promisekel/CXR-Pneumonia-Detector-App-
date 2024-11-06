#from fastai.vision.all import PILImage

#def predict(model, img_path):
 #   img = PILImage.create(img_path)
  #  pred_class, pred_idx, probs = model.predict(img)
   # return pred_class


#def is_xray(model, img_path):
 #   img = PILImage.create(img_path)
  #  pred_class, pred_idx, probs = model.predict(img)
    # Check if the predicted class is in the Xray classes
    #xray_classes = ["PNEUMONIA", "NORMAL"]
    #return pred_class in xray_classes


from fastai.vision.all import PILImage

def predict(model, img_path):
    # Convert img_path to string to ensure compatibility with PILImage
    img = PILImage.create(str(img_path))
    pred_class, pred_idx, probs = model.predict(img)
    return pred_class

def is_xray(model, img_path):
    # Convert img_path to string to ensure compatibility with PILImage
    img = PILImage.create(str(img_path))
    pred_class, pred_idx, probs = model.predict(img)
    # Check if the predicted class is in the X-ray classes
    xray_classes = ["PNEUMONIA", "NORMAL"]
    return pred_class in xray_classes
