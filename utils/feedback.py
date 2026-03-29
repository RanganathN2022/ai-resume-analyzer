def generate_feedback(missing_skills, exp_gap):
    feedback = []

    if missing_skills:
        feedback.append(f"Add missing skills: {', '.join(missing_skills)}")

    if exp_gap > 0:
        feedback.append("Highlight more relevant experience")

    feedback.append("Use action verbs")
    feedback.append("Add measurable achievements")

    return feedback