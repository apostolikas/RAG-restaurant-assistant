# Restaurant Review Local Agent

A lightweight **RAG**-powered web app that answers questions about a French gastropub using real reviews. Built with FastAPI, LangChain, Ollama, and ChromaDB.

## Features
- Retrieve top-k relevant reviews from a local Chroma vector store
- Generate answers using an Ollama LLM (`Llama 3.2` by default)
- Simple, responsive frontend (HTML/CSS/JS)
- One-command local run with FastAPI/Uvicorn

![](https://github.com/apostolikas/RAG-restaurant-assistant/blob/main/demo.png)

## Repo Structure
```
restaurant_review/
├─ api.py                    
├─ vector.py                 
├─ frontend/
│  └─ index.html             
├─ realistic_restaurant_reviews.csv
├─ chroma_langchain_db/     
├─ requirements.txt
├─ demo.png
└─ README.md
```

## Prerequisites
- Python 3.9+
- Ollama installed and running (`ollama serve`)
  - Required models: `llama3.2` and `mxbai-embed-large`
    ```bash
    ollama pull llama3.2
    ollama pull mxbai-embed-large
    ```
- Option A: Use an existing conda env that already has deps
- Option B: Install from `requirements.txt`

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn api:app --host 127.0.0.1 --port 8000 
```

## How it works
- `vector.py` loads `realistic_restaurant_reviews.csv`, builds embeddings with `mxbai-embed-large`, and persists to Chroma (`./chroma_langchain_db`). On first run it adds documents; subsequent runs reuse the DB.
- `api.py` uses a LangChain prompt + `llama3.2` to answer questions, retrieving top-3 relevant reviews from the retriever.
- The frontend posts your question to `/api/ask` and renders the answer + cited reviews.



## Troubleshooting
- Server refuses to connect
  - Ensure it’s running and shows: `Uvicorn running on http://127.0.0.1:8000`
  - Kill any process on port 8000 and retry:
    ```bash
    lsof -ti:8000 | xargs -r kill
    python -m uvicorn api:app --host 127.0.0.1 --port 8000 --reload
    ```
- Missing `uvicorn` or `fastapi`
  - Activate your env or install with `pip install -r requirements.txt`
- Ollama errors / model not found
  - Ensure `ollama serve` is running and models are pulled: `ollama pull llama3.2 mxbai-embed-large`
- Empty answers
  - First run may build the vector DB; wait a moment and retry
  - Check that `realistic_restaurant_reviews.csv` exists and has data
