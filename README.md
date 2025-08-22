# 🎓 AI Career Advisor — Single Agent

Try out the live prototype: [AI Career Advisor Frontend](https://aicareeradvisorfrontend-lpqoeddqgwttzjahdnhuzk.streamlit.app/)

A unified AI-powered assistant that helps users with:
- 💬 Career guidance conversations powered by **LLMs (OpenRouter + DeepSeek)**
- 📚 Personalized **course recommendations** (AI-generated structured JSON)
- 🎯 Real-time **internship & job listings** via **ScrapingDog LinkedIn Jobs API**

---

## 🚀 Tech Stack

- **Backend:** FastAPI (Python), Uvicorn
- **Frontend:** Streamlit (custom Gothic UI)
- **APIs:** OpenRouter (DeepSeek), ScrapingDog (LinkedIn Jobs)
- **Deployment:** Backend on Render, Frontend on Streamlit Cloud
- **Other Tools:** dotenv, requests, humanize

---

## ⚙️ Setup Instructions

### 1. Requirements
- Python 3.10 or newer

### 2. Clone the Repository
```bash
git clone https://github.com/Sauravdas007/AI_Career_Advisor.git
cd AI_Career_Advisor
```

### 3. Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Start Backend (FastAPI)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```
Backend runs at [http://localhost:8000](http://localhost:8000).

### 6. Start Frontend (Streamlit)
```bash
cd frontend
streamlit run streamlit_app.py
```
Frontend runs at [http://localhost:8501](http://localhost:8501).

---

## 🌐 Deployment

- **Backend:** [Render](https://render.com) → deployed as a FastAPI web service  
- **Frontend:** [Streamlit Cloud](https://streamlit.io/cloud) → deployed `streamlit_app.py`  

The frontend connects directly to the backend hosted on Render.

---

## 📂 Project Structure

```
AI_Career_Advisor/
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── requirements.txt
│   └── services/
│       ├── chat_service.py
│       └── internship_service.py
└── README.md
```

---

## ✨ Features

- Gothic dark-themed UI for modern experience  
- Interactive chat with **LLM-driven responses**  
- Real-time **LinkedIn internships & jobs scraping**  
- AI-generated **course suggestions** for upskilling  
- Chat history, pill-style badges, and relative time formatting  

---

## 🔄 Technical Workflow

1. **User enters query** in frontend (Streamlit).  
2. **Backend (FastAPI)** routes request to an **agent handler**.  
3. Depending on intent:  
   - Queries **OpenRouter LLM** → chat or course recommendations  
   - Calls **ScrapingDog API** → LinkedIn internships/jobs  
4. **Results returned** to frontend in structured JSON.  
5. **Streamlit UI renders** chat, courses, or internships dynamically.  

---

## ⚠️ Constraints

- **ScrapingDog API** → 200 free job search calls  
- **OpenRouter API** → 1000 free LLM calls  

Both are subject to free-tier limits of third-party APIs.

---

## 👨‍💻 Contributing

Pull requests welcome! Please open an issue first to discuss changes.

---

Enjoy your AI-powered career journey! 🚀

