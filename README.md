# 🎓 AI Career Advisor — Single Agent

Before reading Try out our live link of prototype: https://aicareeradvisorfrontend-lpqoeddqgwttzjahdnhuzk.streamlit.app/

A unified AI assistant that:
- Chats with users (OpenRouter + DeepSeek)
- Suggests **courses** (LLM-generated structured JSON)
- Finds **internships** via **ScrapingDog LinkedIn Jobs API**

---

## 🚀 Setup Instructions

### 1. **Requirements**
- Python 3.10 or newer recommended

---

### 2. **Clone the Repository**

```bash
git clone https://github.com/Sauravdas007/AI_Career_Advisor.git
cd AI_Career_Advisor
```

---

### 3. **Create & Fill `.env` File**

Create a `.env` file in your project root with content similar to:

```
BACKEND_URL=http://localhost:8000
OPENROUTER_API_KEY=your_openrouter_key
SCRAPINGDOG_API_KEY=your_scrapingdog_key
```
Replace keys with your actual credentials.

---

### 4. **Install Dependencies**

It’s best to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scriptsctivate
pip install -r requirements.txt
```

---

### 5. **Start the Backend (FastAPI)**

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```
This will launch the FastAPI backend at `http://localhost:8000`.

---

### 6. **Start the Frontend (Streamlit UI)**

```bash
cd frontend
streamlit run streamlit_app.py
```
Access the interactive app at [http://localhost:8501](http://localhost:8501).

---

## ☁️ **Deploy for Free**

### **Backend:** [Render.com](https://render.com)
- Connect your backend repo, deploy as a Web Service (see the earlier instructions).

### **Frontend:** [Streamlit Community Cloud](https://streamlit.io/cloud)
- Connect your frontend repo, deploy `streamlit_app.py`.

Set the `BACKEND_URL` in frontend `.env` or secrets to your backend’s public URL after deployment.

---

## 🌐 **Project Structure**

```
my_career_advisor/
├── frontend/
│   ├── __init__.py
│   ├── config.toml
│   ├── streamlit_app.py
│   ├── requirements.txt
├── backend/
│   ├── __init__.py
│   ├── agent.py
│   ├── main.py
│   ├── requirements.txt
│   └── services/
│       ├── __init__.py
│       ├── chat_service.py
│       └── internship_service.py

```

---

## 💡 **Features**

- Custom Gothic dark theme with animated search bar
- Rich chat interface with [OpenRouter (DeepSeek)]
- Real-time internship and course search

---

## 🔒 **Environment Variables**

- `BACKEND_URL` — Where the backend API is hosted
- `OPENROUTER_API_KEY` — For LLM chat
- `SCRAPINGDOG_API_KEY` — For LinkedIn Jobs scraping

Use **Streamlit Cloud “Secrets”** or `.env` for deployment environment variables.

---

## 👨‍💻 **Contributing**

Pull requests welcome! Please open issues first to discuss proposed changes.

---

**Questions or Deployment Help?**  
Open an issue or contact the repo maintainer.

---

Enjoy your AI-powered career journey!
