from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_score(resume_text, job_description):
    """
    Calculate similarity between resume and job description.
    """

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    score = similarity[0][0] * 100

    return round(score, 2)


def find_missing_skills(resume_skills, job_skills):
    """
    Find skills required by the job but missing from the resume.
    """

    resume_skills_lower = {
        skill.lower() for skill in resume_skills
    }

    missing_skills = []

    for skill in job_skills:

        if skill.lower() not in resume_skills_lower:
            missing_skills.append(skill)

    return missing_skills