import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
    "python", "machine learning", "deep learning", "nlp",
    "llm", "generative ai", "langchain", "rag", "transformers",
    "faiss", "sql", "power bi", "mlops", "aws", "azure"
]

SKILL_SYNONYMS = {
    "llm": ["large language model", "large language models"],
    "nlp": ["natural language processing"]
}

def extract_skills(text):
    text = text.lower()
    found = set()

    for skill in SKILLS_DB:
        if skill in text:
            found.add(skill)

    for key, values in SKILL_SYNONYMS.items():
        for val in values:
            if val in text:
                found.add(key)

    return list(found)

SKILL_SYNONYMS = {
    "llm": ["large language model", "large language models"],
    "ml": ["machine learning"],
    "dl": ["deep learning"],
    "nlp": ["natural language processing"]
}

def extract_skills(text):
    text = text.lower()
    found_skills = set()

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.add(skill)

    for key, values in SKILL_SYNONYMS.items():
        for val in values:
            if val in text:
                found_skills.add(key)

    return list(found_skills)