import re

SKILL_KEYWORDS = {
    "python",
    "fastapi",
    "django",
    "flask",
    "java",
    "spring",
    "javascript",
    "typescript",
    "react",
    "node",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "git",
    "rest",
    "api",
    "machine",
    "learning",
    "nlp",
    "data",
    "analysis",
    "pandas",
    "numpy",
}

SKILL_ALIASES = {
    "postgres": "postgresql",
    "js": "javascript",
    "ts": "typescript",
    "k8s": "kubernetes",
}

EXPERIENCE_KEYWORDS = {
    "years",
    "year",
    "senior",
    "junior",
    "lead",
    "manager",
    "project",
    "projects",
    "production",
    "deployment",
    "architecture",
    "scalable",
    "optimize",
    "testing",
    "agile",
    "collaboration",
}


def _tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return {word for word in words if len(word) > 2}


def _normalize_token(word: str) -> str:
    value = SKILL_ALIASES.get(word, word)
    for suffix in ("ing", "ed", "es", "s"):
        if len(value) > 4 and value.endswith(suffix):
            value = value[: -len(suffix)]
            break
    return value


def _normalized_tokens(text: str) -> set[str]:
    return {_normalize_token(token) for token in _tokenize(text)}


def _extract_required_skills(job_description: str) -> set[str]:
    tokens = _normalized_tokens(job_description)
    return {token for token in tokens if token in SKILL_KEYWORDS}


def _extract_resume_skills(resume_text: str) -> set[str]:
    tokens = _normalized_tokens(resume_text)
    return {token for token in tokens if token in SKILL_KEYWORDS}


def _extract_experience_terms(text: str) -> set[str]:
    tokens = _normalized_tokens(text)
    terms = {token for token in tokens if token in EXPERIENCE_KEYWORDS}

    if re.search(r"\b\d+\+?\s*(year|years|yr|yrs)\b", text.lower()):
        terms.add("years")

    return terms


def calculate_match_details(
    resume_text: str,
    job_description: str,
) -> tuple[float, list[str], list[str]]:
    resume_tokens = _normalized_tokens(resume_text)
    job_tokens = _normalized_tokens(job_description)

    if not job_tokens:
        return 0.0, [], []

    required_skills = _extract_required_skills(job_description)
    resume_skills = _extract_resume_skills(resume_text)
    matched_skills = required_skills.intersection(resume_skills)
    matched_skills_sorted = sorted(matched_skills)
    missing_skills = sorted(required_skills.difference(resume_skills))

    if required_skills:
        skills_score = len(matched_skills) / len(required_skills)
    else:
        skills_score = len(resume_tokens.intersection(job_tokens)) / len(job_tokens)

    job_experience_terms = _extract_experience_terms(job_description)
    resume_experience_terms = _extract_experience_terms(resume_text)
    if job_experience_terms:
        experience_score = (
            len(job_experience_terms.intersection(resume_experience_terms))
            / len(job_experience_terms)
        )
    else:
        experience_score = 0.6

    keyword_similarity = len(resume_tokens.intersection(job_tokens)) / len(job_tokens)

    weighted_score = (0.6 * skills_score) + (0.25 * experience_score) + (0.15 * keyword_similarity)
    return round(weighted_score * 100, 2), matched_skills_sorted, missing_skills


def calculate_match_percentage(resume_text: str, job_description: str) -> float:
    score, _, _ = calculate_match_details(resume_text, job_description)
    return score


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
