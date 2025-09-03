from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever


class AskRequest(BaseModel):
    question: str


app = FastAPI(title="Restaurant Review Assistant")

# Allow local development origins (optional if serving same origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static frontend under /app to avoid shadowing /api routes
app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")


# Initialize model and chain once at startup
model = OllamaLLM(model="llama3.2")
template = '''
You are an expert in answering questions about a French gastropub.

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
'''
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/")
def root_redirect():
    return RedirectResponse(url="/app/")


@app.post("/api/ask")
def ask(req: AskRequest):
    question = req.question.strip()
    if not question:
        return JSONResponse(status_code=400, content={"error": "Question is required"})

    reviews = retriever.invoke(question)
    answer = chain.invoke({"reviews": reviews, "question": question})

    # Convert reviews to simple text if they are Document objects
    serialized_reviews = []
    for r in reviews if isinstance(reviews, list) else [reviews]:
        try:
            content = getattr(r, "page_content", str(r))
            metadata = getattr(r, "metadata", {})
            serialized_reviews.append({"content": content, "metadata": metadata})
        except Exception:
            serialized_reviews.append({"content": str(r), "metadata": {}})

    return {
        "answer": answer,
        "question": question,
        "reviews": serialized_reviews,
    }


