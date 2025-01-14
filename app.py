from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for API calls

model = tf.keras.models.load_model('model.h5')

CLASS_LABELS = [
    'Potato - Early Blight',
    'Potato - Late Blight',
    'Potato - Healthy',
    'Tomato - Bacterial Spot',
    'Tomato - Early Blight',
    'Tomato - Late Blight',
    'Tomato - Leaf Mold',
    'Tomato - Septoria Leaf Spot',
    'Tomato - Spider Mites (Two-spotted Spider Mite)',
    'Tomato - Target Spot',
    'Tomato - Yellow Leaf Curl Virus',
    'Tomato - Mosaic Virus',
    'Tomato - Healthy'
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
    try:
        predicted_class = CLASS_LABELS[np.argmax(predictions)]
    except Exception:
        predicted_class = "Cannot be identified"
        confidence = 0
    confidence = float(np.max(predictions))
    return jsonify({'class': predicted_class, 'confidence': confidence})

if __name__ == '__main__':
    app.run(debug=True)
