import re
from nlp.skill_extractor import extract_skills

def parse_job_description(jd_text):
    jd_text = jd_text.lower()

    skills = extract_skills(jd_text)

    # Extract experience (simple regex)
    exp_match = re.findall(r'(\d+)\+?\s*years', jd_text)
    experience = int(exp_match[0]) if exp_match else 0

    return {
        "skills": skills,
        "experience": experience,
        "text": jd_text
    }