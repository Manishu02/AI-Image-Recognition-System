from flask import Flask, render_template, request
from predict import predict_image
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def home():

    image_name = None
    prediction = None
    confidence = None
    predictions = []

    if request.method == "POST":

        image = request.files["image"]

        if image:

            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            image.save(image_path)

            image_name = image.filename

            predictions = predict_image(image_path)

            prediction = predictions[0][0]
            confidence = predictions[0][1]

    return render_template(
        "index.html",
        image_name=image_name,
        prediction=prediction,
        confidence=confidence,
        predictions=predictions
    )


if __name__ == "__main__":
    app.run(debug=True)