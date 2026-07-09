history = []

from flask import Flask, render_template, request , redirect
from predict import predict_image
from pdf_report import create_pdf
from flask import send_file
from datetime import datetime
from PIL import Image
import os
import time

# Allowed image formats
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Maximum file size (5 MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

# Check file extension
def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


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

    image_size = None
    resolution = None
    prediction_time = None

    error = None

    if request.method == "POST":

        image = request.files.get("image")

        # No image selected
        if not image or image.filename == "":
            error = "❌ Please select an image."

        # Invalid file type
        elif not allowed_file(image.filename):
            error = "❌ Please upload only JPG, JPEG or PNG images."

        else:

            # Check file size
            image.seek(0, os.SEEK_END)
            file_size = image.tell()
            image.seek(0)

            if file_size > MAX_FILE_SIZE:
                error = "❌ File size should not exceed 5 MB."

            else:

                image_path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    image.filename
                )

                image.save(image_path)

                image_name = image.filename

                # File Size (KB)
                image_size = round(
                    os.path.getsize(image_path) / 1024,
                    2
                )

                # Resolution
                img = Image.open(image_path)
                resolution = f"{img.width} × {img.height}"

                # Prediction Time
                start = time.time()

                predictions = predict_image(image_path)

                end = time.time()

                prediction_time = round(end - start, 2)

                prediction = predictions[0][0]
                confidence = predictions[0][1]
                print(confidence)
                print(type(confidence))

                # Save History
                history.insert(0,{
                   "id": len(history),
                   "image": image_name,
                   "prediction": prediction,
                   "confidence": confidence,
                   "time": datetime.now().strftime("%I:%M %p"),
                   "path": image_name,

                   "image_size": image_size,
                   "resolution": resolution,
                   "prediction_time": prediction_time
                })

    return render_template(
        "index.html",
        image_name=image_name,
        prediction=prediction,
        confidence=confidence,
        predictions=predictions,
        image_size=image_size,
        resolution=resolution,
        prediction_time=prediction_time,
        history=history,
        error=error
    )
@app.route("/delete-history/<int:item_id>")
def delete_history(item_id):

    global history

    history = [item for item in history if item["id"] != item_id]

    return redirect("/")

@app.route("/clear-history")
def clear_history():

    history.clear()

    return redirect("/")

@app.route("/download-report")
def download_report():

    if not history:
        return "No prediction available."

    latest = history[0]

    pdf_file = create_pdf(
       latest["image"],
       latest["prediction"],
       latest["confidence"],
       latest["image_size"],
       latest["resolution"],
       latest["prediction_time"],
       os.path.join(
        app.config["UPLOAD_FOLDER"],
        latest["path"]
       )
    )

    return send_file(pdf_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)