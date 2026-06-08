from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def calculate_match(resume_skills, jd_text):

    jd_text = jd_text.lower()

    matched = 0

    for skill in resume_skills:
        if skill.lower() in jd_text:
            matched += 1

    if len(resume_skills) == 0:
        return 0

    return int((matched / len(resume_skills)) * 100)