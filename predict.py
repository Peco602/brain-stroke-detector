"""Prediction module"""

import os

import numpy as np
from PIL import Image
from flask import Flask, jsonify, request

if os.path.exists('/.dockerenv'):
    import tflite_runtime.interpreter as tflite
else:
    import tensorflow.lite as tflite


EXPERIMENT_NAME = os.getenv('EXPERIMENT_NAME', 'brain-stroke-detector')
MODEL_PATH = os.getenv('MODEL_PATH', 'data/model.tflite')
TARGET_SIZE = (224, 224)
PREDICT_URL = '/predict'


app = Flask(EXPERIMENT_NAME)

interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']


def prepare_image(file):
    """Creates an image from the webserver input"""
    img = Image.open(file)
    return img


def resize_image(img, target_size):
    """Resizes the image to the target value"""
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img


def preprocess_input(x):
    """Pre-processes the input image"""
    x /= 255
    return x


def predict(file):
    """Performs the prediction"""
    img = prepare_image(file)
    img = resize_image(img, target_size=TARGET_SIZE)

    x = np.array(img, dtype='float32')
    X = np.array([x])

    X = preprocess_input(X)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)
    float_predictions = preds[0].tolist()

    return float_predictions[0] > 0.5


@app.route(PREDICT_URL, methods=["POST"])
def predict_endpoint():
    """Prediction endpoint"""
    try:
        uploaded_img = request.files['img']
        if uploaded_img.filename != '':
            print(f'Received image {uploaded_img.filename}')
            return jsonify({'stroke': predict(uploaded_img)})

    except Exception as e:
        return jsonify({'Error': str(e)})

    return jsonify({'Error': 'Generic error'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
