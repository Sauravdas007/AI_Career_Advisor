import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-chat"

def _openrouter_call(messages, temperature=0.3, max_tokens=800):
    if not OPENROUTER_API_KEY:
        raise RuntimeError("Missing OPENROUTER_API_KEY in environment variables.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=45)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]

async def chat_with_ai(query: str) -> str:
    """
    Freeform chat using OpenRouter (DeepSeek).
    """
    try:
        content = _openrouter_call([
            {"role": "system", "content": "You are a concise, helpful AI career advisor."},
            {"role": "user", "content": query},
        ])
        return content
    except Exception as e:
        return f"⚠️ Chat error: {e}"

async def fetch_courses(query: str):
    """
    Generate course suggestions via the LLM (no external course API).
    We prompt the model to return strict JSON that we can parse into UI cards.
    """
    system = (
        "You are a career advisor that returns strictly valid JSON for course suggestions. "
        "Return an object with key 'results' which is a list of at most 5 items. "
        "Each item must have keys: title, source, rating (number or null), price (string or null), url."
    )
    user = (
        f"User query: {query}\n"
        "Suggest practical, reputable online courses. If unsure, include well-known platforms "
        "(Coursera, edX, Udemy, freeCodeCamp) with realistic links. "
        "Return only JSON. No markdown fences."
    )
    try:
        content = _openrouter_call(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.4,
            max_tokens=900,
        )
        # Parse strict JSON
        data = json.loads(content)
        items = data.get("results", [])
        normalized = []
        for c in items[:5]:
            normalized.append({
                "title": c.get("title") or "Untitled",
                "source": c.get("source") or "Unknown",
                "rating": c.get("rating"),
                "price": c.get("price"),
                "url": c.get("url"),
            })
        return normalized
    except Exception:
        # On any JSON or request failure, gracefully return empty
        return []
