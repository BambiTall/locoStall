from flask import Blueprint, Flask, request, jsonify, make_response
import requests
import os


def send_image_to_model(image_data):
    url = f'http://{os.environ["AI_HOST"]}:{os.environ["AI_PORT"]}/predict'

    try:
        # Send the image as a POST request to the AI model VM
        file = {'file': ('image.jpg', image_data)}
        response = requests.post(url, files=file)

        if response.status_code == 200:
            data = response.json()
            predicted_class = data.get('predicted_class')
            confidence = data.get('confidence')
            return predicted_class, confidence
        else:
            # Handle API error
            return None, None

    except requests.exceptions.RequestException as e:
        # Handle connection or request error
        return None, None


predict_bp = Blueprint('predict_bp', __name__)


# Your API route to handle image processing and prediction
@predict_bp.route(f'{os.environ["API_BASE"]}/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Read the image data from the request directly
        image_data = file.read()

        # Send the image to the model server for prediction
        predicted_class, confidence = send_image_to_model(image_data)

        # Return the prediction result to the frontend or client
        return (
            jsonify({'predicted_class': predicted_class, 'confidence': confidence}),
            200,
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500
