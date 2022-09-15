import streamlit as st
import onnxruntime
import numpy as np
from PIL import Image
from io import BytesIO
import os
import gdown
from static import *

def pred(uploaded_file):
  img = uploaded_file.read()
  img = Image.open(BytesIO(img))
  st.markdown("<h3 style=' color: #666;'>Input Image</h1>", unsafe_allow_html=True)
  st.image(img, caption = uploaded_file.name, channels = "RGB")
  img = img.resize(image_shape)
  
  input = (np.array(img)/255.0-np.array(mean))/np.array(std)
  input = np.expand_dims(np.array(input).transpose(2,0,1),axis=0)
  
  # compute ONNX Runtime output prediction
  input = {plant_model.get_inputs()[0].name: input.astype(np.float32)}
  
  #checking wheather it's plant or not
  classifier_preds = plant_model.run(None, input)
  classifier_max_pred = np.max(np.exp(classifier_preds[0][0])/sum(np.exp(classifier_preds[0][0])))
  
  if (np.argmax(classifier_preds[0][0])==18):
    st.error(f"Please Input a plant image. Thank you.")
    
  elif(np.argmax(classifier_preds[0][0])==4 or (classifier_max_pred*100)<threshold):
    st.error(f"Please Input a supported plant image (Citrus/Potato/Tomato). Thank you.")
    
  else:
    output = labels[np.argmax(classifier_preds[0][0])].title()
    output = output.split(' ')
    st.info(f"Type of Plant: {output[0]} ")
    
    if(output[-1].lower()=="healthy" ):
      st.success(f"Status: {output[-1]}")
      st.warning(f"Probability: {classifier_max_pred*100:.02f}%")
      
    else:
      status = " ".join(output[1:])
      st.error(f"Disease: {status}")
      st.warning(f"Probability: {classifier_max_pred*100:.02f}%")  
      
## App Page
os.makedirs("model",exist_ok = True)
os.makedirs("assets",exist_ok = True) 
  
if not os.path.isfile(model_path):
    model_url = os.environ["MODEL_URL"]
    gdown.download(model_url, model_path, quiet=False)

if not os.path.isfile(fav_path):
    fav_url = os.environ["FAV_URL"]
    gdown.download(fav_url, fav_path, quiet=False)
    
#loading the model
plant_model = onnxruntime.InferenceSession(model_path)

ico = Image.open(fav_path)
st.set_page_config(page_title = title,page_icon=ico)

# Including bootstrap 
st.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">', unsafe_allow_html=True)

# Loading the css file.
with open(style_path) as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


st.title(title)
st.text("Currently only citrus, tomato and potato plant evaluation is available.")
st.write("For more details, source code and test images, see the [github](https://github.com/adnan33/Plant-Disease-Detector-App.git) repository!!!")
uploaded_file = st.file_uploader("Input Plant Leaf Image", type=['jpg','png','jpeg','bmp'])
if (uploaded_file!= None and uploaded_file!=[] ) :
    pred(uploaded_file)
