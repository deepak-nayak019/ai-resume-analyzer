from flask import Flask, request
from werkzeug.utils import secure_filename
import os

from resume_parser import extract_text
from text_processor import clean_text
from skill_extractor import extract_skills


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf", "docx"}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():

    return """
    <h1>AI Resume Analyzer</h1>

    <h2>Upload Your Resume</h2>

    <p>Supported formats: PDF, DOCX</p>

    <form action="/upload" method="POST" enctype="multipart/form-data">

        <input type="file" name="resume" accept=".pdf,.docx">

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
        return "Only PDF and DOCX files are allowed."

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    # Extract resume text
    resume_text = extract_text(filepath)

    cleaned_text = clean_text(resume_text)

    detected_skills = extract_skills(cleaned_text)

    skills_html = ""

    for skill in detected_skills:
        skills_html += f"<li>{skill}</li>"


    return f"""
    <h1>Resume Uploaded Successfully!</h1>

    <h2>Detected Skills</h2>

    <ul>
    {skills_html}
    </ul>

    <h2>Original Resume Text</h2>

    <pre>{resume_text}</pre>

    <h2>Cleaned Resume Text</h2>

    <pre>{cleaned_text}</pre>
    """


if __name__ == "__main__":
    app.run(debug=True)