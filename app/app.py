from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>AI Resume Analyzer</h1>
    <p>Welcome to my AI Resume Analyzer project!</p>
    <p>Project setup is working successfully.</p>
    """


if __name__ == "__main__":
    app.run(debug=True)