from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for API calls

model = tf.keras.models.load_model('model.h5')

CLASS_LABELS = [
                'Potato___Early_blight',
                'Potato___Late_blight',
                'Potato___healthy',
                'Tomato___Bacterial_spot',
                'Tomato___Early_blight',
                'Tomato___Late_blight',
                'Tomato___Leaf_Mold',
                'Tomato___Septoria_leaf_spot',
                'Tomato___Spider_mites Two-spotted_spider_mite',
                'Tomato___Target_Spot',
                'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                'Tomato___Tomato_mosaic_virus',
                'Tomato___healthy'
                ]

def prepare_image(img):
    img = img.resize((256, 256))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    img = Image.open(file).convert('RGB')
    processed_image = prepare_image(img)
    predictions = model.predict(processed_image)
    predicted_class = CLASS_LABELS[np.argmax(predictions)]
    confidence = float(np.max(predictions))
    return jsonify({'class': predicted_class, 'confidence': confidence})

if __name__ == '__main__':
    app.run(debug=True)
