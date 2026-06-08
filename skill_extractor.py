def extract_skills(text):

    skills_db = [
        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "flask",
        "machine learning",
        "git"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills_db:

        if skill in text:
            found_skills.append(skill)

    return found_skills