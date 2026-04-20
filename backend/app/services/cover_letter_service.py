import re


def _top_keywords(job_description: str, limit: int = 3) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+.#-]*", job_description.lower())
    stop_words = {
        "the",
        "and",
        "with",
        "for",
        "you",
        "your",
        "our",
        "are",
        "this",
        "that",
        "will",
        "from",
        "have",
        "has",
        "into",
        "about",
        "experience",
        "years",
        "work",
        "team",
        "role",
        "job",
    }

    counts: dict[str, int] = {}
    for word in words:
        if len(word) < 3 or word in stop_words:
            continue
        counts[word] = counts.get(word, 0) + 1

    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, _ in ranked[:limit]]


def generate_cover_letter(resume_text: str, job_title: str, job_description: str) -> str:
    preview = " ".join(resume_text.strip().split())[:160]
    keywords = _top_keywords(job_description)
    keyword_phrase = ", ".join(keywords) if keywords else "the role requirements"

    lines = [
        f"Dear Hiring Manager,",
        f"I am excited to apply for the {job_title.strip()} position at your organization.",
        "My background and hands-on project work align well with your needs and business goals.",
        f"I can contribute from day one in areas such as {keyword_phrase}.",
        f"My experience summary: {preview}...",
        "Thank you for your time and consideration; I would welcome the opportunity to discuss how I can contribute.",
    ]

    return "\n".join(lines)
