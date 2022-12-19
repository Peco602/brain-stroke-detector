"""Test prediction module"""

import numpy as np
from PIL import Image
from werkzeug.datastructures import FileStorage

import predict

client = predict.app.test_client()


def test_prepare_image():
    """Test image preparation function"""
    with open('data/normal.jpg', 'rb') as fp:
        file = FileStorage(fp)
        predict.prepare_image(file)

    assert True


def test_image_resize():
    """Test image resize function"""
    test_img = Image.new('RGB', size=(1024, 1024), color=(255, 0, 0))
    resized_img = predict.resize_image(test_img, predict.TARGET_SIZE)
    assert resized_img.size == predict.TARGET_SIZE


def test_preprocess_input():
    """Test input preprocessing function"""
    test_img = Image.new('RGB', size=(1024, 1024), color=(255, 0, 0))
    x = np.array(test_img, dtype="float32")
    X = np.array([x])
    X = predict.preprocess_input(X)
    assert X[0][0][0][0] == 1


def test_predict():
    """Test image prediction function"""
    with open('data/normal.jpg', 'rb') as fp:
        file = FileStorage(fp)
        assert not predict.predict(file)

    with open('data/stroke.jpg', 'rb') as fp:
        file = FileStorage(fp)
        assert predict.predict(file)


def test_predict_endpoint():
    """Test predict endpoint"""
    with open('data/normal.jpg', 'rb') as fp:
        sample = {"img": fp}
        response = client.post(predict.PREDICT_URL, data=sample)
        assert not response.json["stroke"]

    with open('data/stroke.jpg', 'rb') as fp:
        sample = {"img": fp}
        response = client.post(predict.PREDICT_URL, data=sample)
        assert response.json["stroke"]

    response = client.post(predict.PREDICT_URL)
    assert "Error" in response.json
