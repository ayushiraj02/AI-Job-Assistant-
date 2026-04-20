import re


def _tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return {word for word in words if len(word) > 2}


def calculate_match_percentage(resume_text: str, job_description: str) -> float:
    resume_tokens = _tokenize(resume_text)
    job_tokens = _tokenize(job_description)

    if not job_tokens:
        return 0.0

    overlap = resume_tokens.intersection(job_tokens)
    score = (len(overlap) / len(job_tokens)) * 100
    return round(score, 2)


def calculate_match_score_from_skills(resume_text: str, job_skills: list[str]) -> float:
    resume_tokens = _tokenize(resume_text)

    normalized_skills = [skill.strip().lower() for skill in job_skills if skill.strip()]
    if not normalized_skills:
        return 0.0

    matched_skills = 0
    for skill in normalized_skills:
        skill_tokens = _tokenize(skill)
        if not skill_tokens:
            continue

        # A skill is counted as matched when all its tokens are present in the resume text.
        if skill_tokens.issubset(resume_tokens):
            matched_skills += 1

    score = (matched_skills / len(normalized_skills)) * 100
    return round(score, 2)
