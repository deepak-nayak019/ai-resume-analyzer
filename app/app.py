from flask import Flask, request
from werkzeug.utils import secure_filename
import os

from resume_parser import extract_text
from text_processor import clean_text
from skill_extractor import extract_skills
from matcher import calculate_match_score, find_missing_skills


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

    <h2>Analyze Your Resume</h2>

    <form action="/analyze" method="POST" enctype="multipart/form-data">

        <label><b>Upload Resume:</b></label>
        <br><br>

        <input type="file"
               name="resume"
               accept=".pdf,.docx"
               required>

        <br><br><br>

        <label><b>Job Description:</b></label>
        <br><br>

        <textarea
            name="job_description"
            rows="12"
            cols="70"
            placeholder="Paste the job description here..."
            required>
        </textarea>

        <br><br>

        <button type="submit">
            Analyze Resume
        </button>

    </form>
    """


@app.route("/analyze", methods=["POST"])
def analyze_resume():

    # Check resume
    if "resume" not in request.files:
        return "Please upload a resume."

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a resume."

    if not allowed_file(file.filename):
        return "Only PDF and DOCX files are allowed."

    # Get job description
    job_description = request.form.get("job_description", "")

    if not job_description.strip():
        return "Please enter a job description."

    # Save resume
    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    # Extract resume text
    resume_text = extract_text(filepath)

    # Clean resume text
    cleaned_resume = clean_text(resume_text)

    # Clean job description
    cleaned_job = clean_text(job_description)

    # Extract resume skills
    resume_skills = extract_skills(cleaned_resume)

    # Extract job skills
    job_skills = extract_skills(cleaned_job)

    # Calculate match score
    match_score = calculate_match_score(
        cleaned_resume,
        cleaned_job
    )

    # Find missing skills
    missing_skills = find_missing_skills(
        resume_skills,
        job_skills
    )

    # Display matching skills
    matching_skills = [
        skill for skill in job_skills
        if skill.lower() in {
            s.lower() for s in resume_skills
        }
    ]

    return f"""
    <h1>Resume Analysis Result</h1>

    <h2>Resume Match Score</h2>

    <h1>{match_score}%</h1>

    <h2>Matching Skills</h2>

    <ul>
        {"".join(f"<li>✓ {skill}</li>" for skill in matching_skills)}
    </ul>

    <h2>Missing Skills</h2>

    <ul>
        {"".join(f"<li>✗ {skill}</li>" for skill in missing_skills)}
    </ul>

    <br>

    <a href="/">
        Analyze Another Resume
    </a>
    """


if __name__ == "__main__":
    app.run(debug=True)