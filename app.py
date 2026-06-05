from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os

from fnst import Stylizer

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/stylize', methods=['POST'])
def stylize():

    try:

        image = request.files['image']
        style = request.form['style']

        filename = secure_filename(image.filename)

        input_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        image.save(input_path)

        # Select model
        if style == "candy":
            model_path = "models/candy.pth"

        elif style == "mosaic":
            model_path = "models/mosaic.pth"

        elif style == "picasso":
            model_path = "models/picasso.pth"

        else:
            return "Invalid style selected", 400

        # Run Style Transfer
        stylizer = Stylizer(
            model_path=model_path,
            output_path=OUTPUT_FOLDER
        )

        output_path = stylizer.stylize(input_path)

        if not os.path.exists(output_path):
            return "Output image not generated", 500

        return send_file(
            output_path,
            mimetype='image/jpeg'
        )

    except Exception as e:
        print("ERROR:", str(e))
        return str(e), 500


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )