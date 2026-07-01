from flask import Flask, render_template, request, send_file
import os

from crypto_engine import encrypt_file, decrypt_file

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/encrypt", methods=["POST"])
def encrypt():

    file = request.files["file"]
    password = request.form["password"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(filepath)

    output_file = encrypt_file(
        filepath,
        password,
        OUTPUT_FOLDER
    )

    return send_file(
        output_file,
        as_attachment=True
    )


@app.route("/decrypt", methods=["POST"])
def decrypt():

    file = request.files["file"]
    password = request.form["password"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(filepath)

    output_file = decrypt_file(
        filepath,
        password,
        OUTPUT_FOLDER
    )

    return send_file(
        output_file,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)