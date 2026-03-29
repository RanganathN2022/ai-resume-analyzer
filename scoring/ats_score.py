def calculate_ats(skill_match, exp_match, keyword_match, edu_match, formatting):
    score = (
        0.4 * skill_match +
        0.2 * exp_match +
        0.2 * keyword_match +
        0.1 * edu_match +
        0.1 * formatting
    )
    return round(score * 100, 2)