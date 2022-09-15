image_shape = (299,299)
mean=[0.485, 0.456, 0.406]
std=[0.229, 0.224, 0.225]
threshold = 90.0

title = "Plant Disease Detector"

labels = ['Citrus Black spot', 'Citrus Healthy', 'Citrus canker', 'Citrus greening','Other_Plants', 'Potato Early blight',
          'Potato Healthy', 'Potato Late blight', 'Tomato Bacterial spot', 'Tomato Early blight',
          'Tomato Healthy', 'Tomato Late blight', 'Tomato Leaf Mold', 'Tomato Mosaic virus',
          'Tomato Septoria leaf spot', 'Tomato Spider mites', 
          'Tomato Target Spot', 'Tomato Yellow Leaf Curl Virus', 'not_plant']

style_path = "css/style.css"

model_url = ""

fav_url = ""

fav_path = "assets/leaf-256.ico"

model_path = "model/plant_classifier_model.onnx"



