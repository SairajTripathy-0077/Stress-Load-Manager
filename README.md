# 📊 Stress Load Manager (Pathway-Inspired)

A **real-time academic workload monitoring and AI planning system** inspired by **Pathway’s streaming data paradigm**.  
This project ingests student workload data (assignments, exams, events), maintains a live workload state, and uses an **LLM** to generate **human-friendly plans, stress insights, and actionable guidance**.

---

## 🚀 Problem Statement

Students often struggle to:
- Track multiple assignments, exams, and events
- Understand workload intensity
- Prioritize tasks based on urgency
- Reduce stress with structured planning

Most existing tools are **static**, require refresh, or lack intelligent reasoning.

---

## 💡 Solution

**Stress Load Manager** provides:
- Live data ingestion from UI
- Real-time workload aggregation
- Persistent backend storage
- AI-powered planning and stress analysis
- Pathway-style continuous updates (no refresh)

---

## 🧠 Why Pathway-Inspired?

This project follows Pathway’s core concepts:

| Pathway Concept | This Project |
|-----------------|-------------|
| Streaming ingestion | Live UI ingestion |
| Stateful processing | Persistent JSON store |
| Incremental updates | No refresh UI updates |
| Declarative logic | Central workload facts |
| Real-time reasoning | LLM answers from live data |

---

Frontend (React + Vite)
│
│ Ingest / Edit / Delete (Live)
│
▼
FastAPI Backend
│
├── Ingestion Layer
├── Storage Layer (JSON)
├── Workload Aggregator
└── LLM Reasoning Engine


---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn
- JSON storage

### Frontend
- React
- Vite
- JavaScript

### AI
- LLM (Gemini / OpenAI compatible)
- Prompt-driven reasoning

### Hosting
- Render (Free Tier)

---

## 📁 Project Structure

Stress-Load-Manager/
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ │ ├── IngestForm.jsx
│ │ │ ├── LiveData.jsx
│ │ │ └── AskAI.jsx
│ │ ├── api.js
│ │ ├── App.jsx
│ │ └── main.jsx
│
├── pathway-engine/
│ ├── main.py
│ ├── ingestions.py
│ ├── workload.py
│ ├── storage.py
│ ├── llm.py
│ ├── data_store.json
│ └── requirements.txt
│
└── README.md


---

## 🔄 How It Works

1. User ingests assignments/exams/events from UI  
2. Backend stores data persistently  
3. Workload facts are recalculated in real-time  
4. AI uses live workload data to generate plans  
5. UI updates instantly without refresh  

---

## 🧪 API Endpoints

### Ingest Data

### Get Live Data

### Update Item

### Ask AI

### Delete Item


---

Link of the website ("https://student-workload-manager.netlify.app/")


## 🧱 Architecture Overview

