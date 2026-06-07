from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import anthropic
import warnings
import json
import re
warnings.filterwarnings("ignore")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load vector database once on startup
print("Loading research database...")
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./db", embedding_function=embeddings)
print("Database ready.")

class DiagnoseRequest(BaseModel):
    exercise: str
    experience: str
    weightReps: str
    duration: str
    failurePoint: str
    frequency: str
    context: str
    goal: str

class ChatRequest(BaseModel):
    message: str
    history: list
    diagnosisSummary: str

@app.get("/")
async def serve_index():
    return FileResponse("plateau-breaker.html")

@app.post("/diagnose")
async def diagnose(req: DiagnoseRequest):
    # Search for relevant research
    query = f"{req.exercise} plateau {req.goal} {req.failurePoint} progressive overload"
    results = db.similarity_search(query, k=3)
    research = "\n\n".join([doc.page_content for doc in results])

    system_prompt = f"""You are a knowledgeable, friendly strength coach who gives specific, evidence-based advice.

Adapt your tone based on experience level:
- BEGINNER (under 1 year): simple language, explain terms, encouraging
- INTERMEDIATE (1-3 years): friendly and practical, some technical terms  
- ADVANCED (3+ years): technical, direct, no hand-holding

Here is relevant research to base your diagnosis on:
---
{research}
---

Respond ONLY with a raw JSON object, no markdown, no backticks:
{{"why":"...","protocol":"...","watch":"..."}}

- why: 2-4 sentences on root cause, reference the research where relevant
- protocol: specific 3-4 week plan with sets, reps, percentages, use line breaks
- watch: 2-3 sentences on what to avoid"""

    user_prompt = f"""Exercise: {req.exercise}
Experience: {req.experience}
Weight/reps: {req.weightReps}
Stuck for: {req.duration}
Failure point: {req.failurePoint}
Frequency: {req.frequency}
Context: {req.context}
Goal: {req.goal}"""

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1200,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )

    raw = message.content[0].text.strip()
    match = re.search(r'\{[\s\S]*\}', raw)
    parsed = json.loads(match.group())
    return parsed

@app.post("/chat")
async def chat(req: ChatRequest):
    system_prompt = f"""You are a strength coach who already gave a plateau diagnosis. Answer follow-up questions briefly — 2-4 sentences max. Be direct and practical.

Original diagnosis context:
{req.diagnosisSummary}"""

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=system_prompt,
        messages=req.history
    )

    return {"reply": message.content[0].text.strip()}



