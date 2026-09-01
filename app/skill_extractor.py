import csv
import re


SKILLS_FILE = "data/skills.csv"


def load_skills():
    """
    Load skills from the skills CSV file.
    """

    skills = []

    with open(SKILLS_FILE, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            skills.append(row["skill"])

    return skills


def extract_skills(text):
    """
    Find known skills in resume text.
    """

    skills = load_skills()

    found_skills = []

    for skill in skills:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text.lower()):

            found_skills.append(skill)

    return found_skills