from flask import Flask, request
from werkzeug.utils import secure_filename
import os

from resume_parser import extract_text_from_pdf


app = Flask(__name__)

# Folder where uploaded resumes will be stored
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Maximum file size: 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    """
    Check whether the uploaded file is a PDF.
    """

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():

    return """
    <h1>AI Resume Analyzer</h1>

    <h2>Upload Your Resume</h2>

    <form action="/upload" method="POST" enctype="multipart/form-data">

        <input type="file" name="resume" accept=".pdf">

        <br><br>

        <button type="submit">Upload Resume</button>

    </form>
    """


@app.route("/upload", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return "No resume file was selected."

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a resume."

    if not allowed_file(file.filename):
        return "Only PDF files are allowed."

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    # Extract text from PDF
    resume_text = extract_text_from_pdf(filepath)

    return f"""
    <h1>Resume Uploaded Successfully!</h1>

    <h2>Extracted Resume Text</h2>

    <pre>{resume_text}</pre>
    """


if __name__ == "__main__":
    app.run(debug=True)