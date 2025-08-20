import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root (one level up from backend/)
project_root = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=project_root / ".env")

from agent import agent_handler

app = FastAPI(title="AI Career Advisor — Single Agent")

# CORS: open for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health():
    return {"status": "ok"}

@app.get("/agent")
async def agent_endpoint(query: str):
    """
    Unified endpoint: routes to either chat, courses (LLM-generated),
    or internships (ScrapingDog LinkedIn Jobs).
    """
    return await agent_handler(query)
