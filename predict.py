import tensorflow as tf
import numpy as np
import cv2

from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)
from tensorflow.keras.preprocessing import image

model = MobileNetV2(weights="imagenet")

def predict_image(img_path):

    img_cv = cv2.imread(img_path)

    img_cv = cv2.resize(img_cv, (224, 224))

    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    x = np.array(img_cv)

    x = np.expand_dims(x, axis=0)

    x = preprocess_input(x)

    predictions = model.predict(x)

    results = decode_predictions(predictions, top=5)[0]

    prediction_list = []

    for result in results:

        label = result[1].replace("_", " ").title()
        confidence = round(result[2] * 100, 2)

        prediction_list.append((label, confidence))

    return prediction_list