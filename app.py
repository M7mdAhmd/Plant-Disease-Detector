import cv2
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import models, layers
from tensorflow.keras.applications.efficientnet import EfficientNetB0, preprocess_input
from flask import Flask, render_template, request
from flask_cors import CORS

base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model= models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(1024, activation = 'relu'),
    layers.Dense(1024, activation = 'relu'),
    layers.Dropout(0.3),
    layers.Dense(512, activation = 'relu'),
    layers.Dense(512, activation = 'relu'),
    layers.Dense(38, activation = 'softmax')
])
# Newer Keras versions (e.g., 3.11+) have a bug where EfficientNet incorrectly assumes grayscale (1-channel)
# input instead of RGB (3-channel), causing a shape mismatch error when loading pre-trained ImageNet weights.
# so use Keras version below 3.10

model.build((None, 224, 224, 3))
model_path = os.path.join(os.getcwd(), 'model.keras')
model.load_weights(model_path)

class_names = ['Apple Apple scab', 'Apple Black rot', 'Apple Cedar apple rust', 'Apple healthy',
'Blueberry healthy', 'Cherry (including sour) Powdery mildew', 'Cherry (including sour) healthy',
'Corn (maize) Cercospora leaf spot Gray leaf spot', 'Corn (maize) Common rust ', 'Corn (maize) Northern Leaf Blight',
'Corn (maize) healthy', 'Grape Black rot', 'Grape Esca (Black Measles)', 'Grape Leaf blight (Isariopsis Leaf Spot)',
'Grape healthy', 'Orange Haunglongbing (Citrus greening)', 'Peach Bacterial spot', 'Peach healthy', 
'Pepper, bell Bacterial spot', 'Pepper, bell healthy', 'Potato Early blight', 'Potato Late blight',
'Potato healthy', 'Raspberry healthy', 'Soybean healthy', 'Squash Powdery mildew', 'Strawberry Leaf scorch',
'Strawberry healthy', 'Tomato Bacterial spot', 'Tomato Early blight', 'Tomato Late blight', 'Tomato Leaf Mold',
'Tomato Septoria leaf spot', 'Tomato Spider mites Two-spotted spider mite', 'Tomato Target Spot',
'Tomato Tomato Yellow Leaf Curl Virus', 'Tomato Tomato mosaic virus', 'Tomato healthy']

def predict(file):
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    test_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    test_image = cv2.resize(test_image, (224, 224))
    test_image = np.expand_dims(test_image, 0)
    test_image = preprocess_input(test_image.astype(np.float32))
    probs = model.predict(test_image)
    class_index = np.argmax(probs)
    image_class = class_names[class_index]
    return image_class


app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

@app.route('/', methods = ['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        file = request.files.get('file')
        if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            predicted_class = predict(file)
        else:
            predicted_class = ''
        
        return render_template('index.html', result = predicted_class)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)