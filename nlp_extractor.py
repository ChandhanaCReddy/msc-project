import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_resume_details(text):

    doc = nlp(text)

    details = {
        "name": "",
        "email": "",
        "phone": "",
        "education": [],
        "organizations": [],
        "skills": []
    }
    # -------- Name --------

    lines = text.split("\n")

    for line in lines[:5]:

        line = line.strip()

        if (
            len(line.split()) >= 2
            and len(line.split()) <= 3
            and '@' not in line
            and not any(char.isdigit() for char in line)
            and "summary" not in line.lower()
            and "objective" not in line.lower()
            and "resume" not in line.lower()
            and "profile" not in line.lower()
        ):
            details["name"] = line.title()
            break
    # -------- Email --------
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    emails = re.findall(email_pattern, text)

    if emails:
        details["email"] = emails[0]

    # -------- Phone --------
    phone_pattern = r'\+?\d[\d\-\s]{8,15}\d'
    phones = re.findall(phone_pattern, text)

    if phones:
        details["phone"] = phones[0]

    # -------- Organizations --------
    for ent in doc.ents:

        if ent.label_ == "ORG":

            if ent.text not in details["organizations"]:
                details["organizations"].append(ent.text)

    # -------- Education --------
    education_keywords = [
        "b.tech",
        "b.e",
        "bsc",
        "bca",
        "m.tech",
        "mca",
        "msc",
        "mba",
        "phd"
    ]

    text_lower = text.lower()

    for edu in education_keywords:

        if edu in text_lower:
            details["education"].append(edu.upper())

    # -------- Skills --------
    skills_db = [

        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "react",
        "flask",
        "django",
        "machine learning",
        "deep learning",
        "data analysis",
        "power bi",
        "excel",
        "git",
        "aws",
        "docker"
    ]

    for skill in skills_db:

        if skill.lower() in text_lower:
            details["skills"].append(skill)

    return details