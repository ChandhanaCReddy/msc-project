import spacy

nlp = spacy.load("en_core_web_sm")

def extract_skills(text):

    doc = nlp(text)

    skills = set()

    for chunk in doc.noun_chunks:

        phrase = chunk.text.strip()

        if (
            len(phrase.split()) <= 4
            and len(phrase) > 2
        ):
            skills.add(phrase)

    for ent in doc.ents:

        if ent.label_ in ["ORG", "PRODUCT"]:

            skills.add(ent.text.strip())

    return list(skills)