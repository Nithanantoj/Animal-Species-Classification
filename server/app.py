from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from flask_cors import CORS  # Importing CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Load the pre-trained model
model = load_model('model/animal_species_classifier.h5')
print("Model loaded successfully")

# Class labels
CLASS_LABELS = ['Cat', 'Dog', 'Snake']


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.content_type.startswith('image/'):
        return jsonify({'error': 'Unsupported file type'}), 400

    try:
        # Preprocess the image
        img = Image.open(file).resize((128, 128))  # Update size based on your model
        img_array = np.array(img) / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0)

        # Make prediction
        predictions = model.predict(img_array)
        class_index = np.argmax(predictions)
        class_name = CLASS_LABELS[class_index]
        confidence = float(predictions[0][class_index])

        print(f"Predicted class index: {class_index}")
        print(f"Predicted class name: {class_name}")
        print(f"Confidence: {confidence}")

        return jsonify({'class': class_name, 'confidence': confidence})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing the image. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
