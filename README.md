# Plateau Breaker

A strength training plateau diagnosis tool, informed by peer-reviewed sports science research.

## How it works

1. Answer 7 questions about your stuck lift — exercise, current weight, failure point, frequency, context, goal
2. A FastAPI backend retrieves relevant sports science research using semantic search (RAG)
3. Claude synthesizes the research with your specific situation to generate a diagnosis
4. You get three outputs: why you're stuck, a 3-4 week protocol, and what to watch out for
5. A follow-up chat lets you ask questions about your diagnosis

## Tech stack

- **Frontend** — Vanilla JS, HTML/CSS, deployed on Cloudflare Pages
- **Backend** — Python, FastAPI, deployed on Railway
- **AI** — Anthropic Claude
- **RAG** — Semantic search over peer-reviewed sports science studies

## Live demo

https://plateau-breaker.pages.dev

## Related

[Form Analyzer](https://plateau-breaker.pages.dev/form-analyzer.html) — upload a video of your lift for computer vision form analysis
