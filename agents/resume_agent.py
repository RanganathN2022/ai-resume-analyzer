from nlp.skill_extractor import extract_skills

def generate_suggestions(missing_skills):
    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Consider adding experience or projects related to '{skill}'")

    return suggestions


def rewrite_bullets(resume_text):
    """
    Simulate improved bullet points (rule-based)
    """
    improved_points = [
        "Developed machine learning models improving accuracy by 20%",
        "Implemented NLP pipelines for real-world applications",
        "Built scalable AI solutions using Python and cloud tools"
    ]

    return improved_points


def run_resume_agent(resume_text, jd_text, jd_skills):

    history = []

    # Step 1: Analyze
    resume_skills = extract_skills(resume_text)
    missing_skills = list(set(jd_skills) - set(resume_skills))

    history.append({
        "step": "Analysis",
        "skills": resume_skills,
        "missing": missing_skills
    })

    # Step 2: Suggestions
    suggestions = generate_suggestions(missing_skills)

    history.append({
        "step": "Suggestions",
        "suggestions": suggestions
    })

    # Step 3: Bullet Improvements
    improved_bullets = rewrite_bullets(resume_text)

    history.append({
        "step": "Bullet Improvement",
        "bullets": improved_bullets
    })

    return {
        "original_skills": resume_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "bullets": improved_bullets,
        "history": history
    }