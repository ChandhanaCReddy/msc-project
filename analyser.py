def analyze_resume(skills):

    required_skills = [
        "python",
        "sql",
        "html",
        "css",
        "javascript",
        "git"
    ]

    matched = 0
    missing = []

    for skill in required_skills:

        if skill in skills:
            matched += 1
        else:
            missing.append(skill)

    score = int((matched / len(required_skills)) * 100)

    return score, missing