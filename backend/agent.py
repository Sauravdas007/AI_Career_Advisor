from services.chat_service import chat_with_ai, fetch_courses
from services.internship_service import fetch_internships

COURSE_KEYWORDS = {
    "course", "courses", "learn", "learning", "study", "curriculum",
    "syllabus", "skills", "upskill", "certificate", "certification", "bootcamp", "mooc"
}

INTERN_KEYWORDS = {
    "intern", "internship", "internships", "summer", "placement", "apprentice",
    "job", "jobs", "hiring", "opening"
}

def _intent_from_text(text: str) -> str:
    t = text.lower()
    if any(k in t for k in INTERN_KEYWORDS):
        return "internships"
    if any(k in t for k in COURSE_KEYWORDS):
        return "courses"
    return "chat"

def _extract_field_and_location(user_query: str):
    """
    Heuristic extraction for internships:
    - field: few key tokens before the word 'intern'/'job'
    - location: prepositions like 'in <city>' or 'at <city>' if present
    This is intentionally simple; you can replace with an LLM or regex as needed.
    """
    import re
    t = user_query.strip()
    # Location
    m = re.search(r"\b(?:in|at)\s+([A-Za-z ,._-]+)$", t, flags=re.IGNORECASE)
    location = m.group(1).strip() if m else ""
    # Field: words before 'intern' or 'job'
    m2 = re.search(r"(.+?)\b(?:intern(?:ship)?|job|jobs)\b", t, flags=re.IGNORECASE)
    field = m2.group(1).strip() if m2 else t
    # Cleanup
    field = re.sub(r"\b(find|looking for|search|searching|need|want|show|give me)\b", "", field, flags=re.IGNORECASE).strip()
    return field or "software", location or ""

async def agent_handler(user_query: str):
    intent = _intent_from_text(user_query)

    if intent == "courses":
        results = await fetch_courses(user_query)
        if results:
            return {"type": "courses", "results": results}
        # fallback to chat if no structured results
        reply = await chat_with_ai(user_query)
        return {"type": "chat", "reply": reply}

    if intent == "internships":
        field, location = _extract_field_and_location(user_query)
        results = await fetch_internships(field=field, location=location or "Worldwide")
        return {"type": "internships", "results": results}

    # default to freeform chat
    reply = await chat_with_ai(user_query)
    return {"type": "chat", "reply": reply}
