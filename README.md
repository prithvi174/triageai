# TriageAI

**LLM-powered IT support ticket classifier** — takes a raw ticket description and returns its category, priority, and suggested team, with a confidence score and reasoning.

## The problem

IT helpdesks deal with a constant stream of unsorted tickets. Someone has to read each one, figure out what it's about, decide how urgent it is, and route it to the right team — usually manually, which is slow and inconsistent, especially during high volume (e.g. an outage flooding the queue with duplicate/related tickets).

This project explores whether an LLM can do that first triage pass reliably — not to replace a human, but to cut down the time spent on initial sorting.

*Inspired by ticket-routing challenges I saw during my internship at NTT Data — this is a personal, from-scratch rebuild with no proprietary code or data.*

## How it works

<img width="1000" height="818" alt="assetsdemo_screenshot png" src="https://github.com/user-attachments/assets/9c8ca0b4-6603-48b3-9e50-4613edc6f45f" />


1. You submit a raw ticket description (e.g. *"VPN keeps disconnecting every 5 minutes"*)
2. FastAPI passes it to Groq's LLaMA 3.3 70B with a system prompt defining the classification rules
3. The LLM returns JSON, which gets validated against a strict Pydantic schema (category, priority, team — all constrained to fixed enums, so the model can't return anything invalid)
4. The result is shown in the UI with a confidence score and the model's reasoning

## Tech stack

- **Backend:** FastAPI, Pydantic
- **LLM:** Groq API (LLaMA 3.3 70B)
- **Frontend:** Streamlit
- **Language:** Python

## Running it locally

1. Clone the repo and install dependencies:

```bash
pip install -r requirements.txt
```

2. Add your Groq API key:

```bash
cp .env.example .env
```

Then edit `.env` and add your key.

3. Start the backend:

```bash
uvicorn app:app --reload
```

4. In a separate terminal, start the UI:

```bash
streamlit run ui/streamlit_app.py
```

5. Open `http://localhost:8501` and try it out.

## Example

**Input:**

> "VPN keeps disconnecting every 5 minutes while working from home, very disruptive."

**Output:**

| Field | Value |
|---|---|
| Category | Network |
| Priority | High |
| Suggested Team | Network Ops |
| Confidence | 0.9 |
| Reasoning | Related to VPN connectivity, a network issue affecting the user's core work — high priority. |

## Design notes

- **Enum-constrained schema** — category/priority/team are Pydantic enums, not free text. This forces the LLM's output into a fixed set of values and makes downstream logic (routing, dashboards) reliable.
- **Layered error handling** — the classifier distinguishes between malformed LLM output (invalid JSON) and valid JSON that fails schema validation (e.g. the model invents a category). The API layer does the same for its own failure modes. This came directly out of a debugging lesson from my internship — a bare `except` there once silently swallowed errors and made a bug much harder to trace.
- **Frontend/backend split** — the UI calls the API over HTTP rather than importing the classifier directly, so either layer can be swapped or scaled independently.

## Status / roadmap

This is an actively evolving personal project, not a production system. Currently exploring:

- Batch classification (CSV upload)
- Confidence-based flagging for human review
- Duplicate ticket detection via embeddings

## Disclaimer

This project uses synthetic ticket data for testing and demonstration. It is not connected
