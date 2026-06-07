# Plateau Breaker

**Live site → [plateau-breaker.pages.dev](https://plateau-breaker.pages.dev)**

A web app that diagnoses weightlifting plateaus using AI and peer-reviewed sports science research. Answer 8 questions about your stuck lift and get a specific, evidence-based plan to break through.

---

## How it works

1. User answers 8 questions about their plateau (exercise, experience level, failure point, frequency etc.)
2. The backend searches a vector database of sports science studies for the most relevant research
3. That research is injected into a prompt sent to Claude (Anthropic)
4. Claude returns a structured diagnosis — why you're stuck, a 3-4 week protocol, and what to avoid
5. A follow-up chat lets users ask questions about their diagnosis

The response tone adapts automatically based on experience level — simpler language for beginners, technical terminology for advanced lifters.

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| AI | Claude API (Anthropic) |
| RAG pipeline | LangChain, ChromaDB, Sentence Transformers |
| Frontend hosting | Cloudflare Pages |
| Backend hosting | Railway |

---

## Running locally

```bash
# Clone the repo
git clone https://github.com/davidmenkreo07/Plateau-Breaker.git
cd Plateau-Breaker

# Create and activate environment
conda create -n plateau-rag python=3.11
conda activate plateau-rag

# Install dependencies
pip install -r requirements.txt

# Build the research database
python3 ingest.py

# Start the server
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000` in your browser.

---

## Adding research

Drop PDF studies into the `studies/` folder and run:

```bash
python3 ingest.py
```

The database updates automatically.
