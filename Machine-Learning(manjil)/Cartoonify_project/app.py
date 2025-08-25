from flask import Flask, render_template, request, send_from_directory
import os
from cartoonify import cartoonify_image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Home page (upload form)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            output_path = os.path.join(app.config["UPLOAD_FOLDER"], "cartoon_" + file.filename)
            cartoonify_image(filepath, output_path)

            return render_template("result.html", original=file.filename, cartoon="cartoon_" + file.filename)

    return render_template("index.html")

# Serve uploaded files
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)


