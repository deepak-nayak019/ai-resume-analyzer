import re


def clean_text(text):
    """
    Clean extracted resume text for NLP processing.
    """

    # Convert text to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", "", text)

    # Keep letters, numbers, and basic spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove spaces from beginning and end
    text = text.strip()

    return text