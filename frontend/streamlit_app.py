import os
from pathlib import Path
import requests
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime, timezone
from dateutil import parser as date_parser
import humanize

# ========== Gothic Style ==========
st.set_page_config(
    page_title="🎓 AI Career Advisor",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=UnifrakturCook:wght@700&display=swap');
        .gothic-title {
            font-family: 'UnifrakturCook', cursive;
            font-size: 2.6rem;
            color: #ad1f2d;
            text-shadow: 3px 3px 7px #00000077;
            letter-spacing: 2px;
            padding-bottom: 10px;
        }
        .big-input textarea {
            min-height: 60px !important;
            font-size: 1.20em !important;
            border-radius: 12px !important;
            background: #2c2230 !important;
            color: #e6e1ea !important;
            box-shadow: 0 0 10px #ad1f2d55;
            border: 1.5px solid #ad1f2d !important;
            font-family: 'UnifrakturCook', cursive;
        }
        .st-c4, .stContainer {background: transparent !important;}
        .stChatInputContainer textarea {font-size:1.2em;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="gothic-title">🎓 AI Career Advisor</div>', unsafe_allow_html=True)
st.caption("Ask about careers. Say 'courses for X' or 'internship in Y' to fetch structured results.")

# ========== Setup ==========
project_root = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=project_root / ".env")
BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

# ========== Helpers ==========
def render_chat(role: str, content: str):
    with st.chat_message(role):
        st.markdown(content)

def fetch_backend(query: str) -> dict:
    try:
        resp = requests.get(f"{BACKEND}/agent", params={"query": query}, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"type": "chat", "reply": f"⚠️ Backend error: {e}"}

def relative_time(date_str: str) -> str | None:
    if not date_str:
        return None
    try:
        dt = date_parser.parse(date_str)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return f"Posted {humanize.naturaltime(datetime.now(timezone.utc) - dt)}"
    except Exception:
        return date_str

def pill(label: str) -> str:
    if not label:
        return ""
    return f"""
    <span style="
        display:inline-block;
        padding:2px 8px;margin:2px 6px 0 0;
        border-radius:999px;
        background-color:#522c37;
        font-size:0.85em;line-height:1.8;
        color:#e6e1ea;
        border:1px solid #ad1f2d;">
        {label}
    </span>
    """

def render_courses(items: list):
    intro = "Here are some courses that fit your query:" if items else "No courses found."
    render_chat("assistant", intro)
    if not items:
        return
    with st.expander("📚 View suggested courses"):
        for c in items:
            with st.container(border=True):
                st.markdown(f"**{c.get('title','Untitled')}**")
                badges = "".join(pill(x) for x in [
                    c.get("source"),
                    f"⭐ {c.get('rating')}" if c.get("rating") else None,
                    c.get("price"),
                ] if x)
                if badges:
                    st.markdown(badges, unsafe_allow_html=True)
                if c.get("url"):
                    st.link_button("Open Course", c["url"])

def render_internships(items: list):
    intro = "Here are internship opportunities I found:" if items else "No internships found."
    render_chat("assistant", intro)
    if not items:
        return
    with st.expander("🎯 View internship matches"):
        for j in items:
            with st.container(border=True):
                st.markdown(f"**{j.get('title','Internship')}** — {j.get('company','Unknown')}")
                badges = "".join(pill(x) for x in [
                    j.get("location"),
                    j.get("site"),
                    relative_time(j.get("date_posted")),
                ] if x)
                if badges:
                    st.markdown(badges, unsafe_allow_html=True)
                if j.get("url"):
                    st.link_button("Open Listing", j["url"])

# ========== Chat History ==========
if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    render_chat(msg["role"], msg["content"])

# ========== Main Input ==========
with st.form("chat_form", clear_on_submit=True):
    user_msg = st.text_area(
        "", 
        placeholder="e.g., 'frontend internship in Mumbai' or 'courses for data analysis'",
        key="chat_input",
        height=60
    )
    st.form_submit_button("Send")
st.markdown(
    "<script>document.querySelectorAll('textarea')[0].classList.add('big-input');</script>",
    unsafe_allow_html=True
)

if user_msg:
    st.session_state.history.append({"role": "user", "content": user_msg})
    render_chat("user", user_msg)

    data = fetch_backend(user_msg)

    if data.get("type") == "chat":
        reply = data.get("reply", "(no reply)")
        st.session_state.history.append({"role": "assistant", "content": reply})
        render_chat("assistant", reply)
    elif data.get("type") == "courses":
        render_courses(data.get("results", []))
    elif data.get("type") == "internships":
        render_internships(data.get("results", []))

# ========== Footer ==========
st.markdown("---")
st.caption("⚡ Powered by FastAPI backend • OpenRouter (DeepSeek) for chat • ScrapingDog for LinkedIn jobs")
