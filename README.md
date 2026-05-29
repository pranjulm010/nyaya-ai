# Nyaya AI — Indian Legal Intelligence Platform

## What Is Nyaya AI?

Nyaya AI is an AI-powered legal research and document analysis platform built specifically for the Indian legal ecosystem. It allows law firms, advocates, legal departments, and compliance teams to upload legal documents (contracts, FIRs, judgments, notices) and ask plain-language questions — receiving detailed, sourced answers drawn from the document itself, Indian case law databases, and live legal news sources.

---

## Business Requirements

### The Problem It Solves

Legal research in India is time-intensive and fragmented. An advocate or in-house counsel typically spends 4–8 hours manually searching Indian Kanoon, reading through PDF judgments, and cross-referencing legislation for a single case. Nyaya AI compresses that to minutes.

### Core Use Cases

| Use Case | Who Benefits |
|---|---|
| Contract review and clause analysis | Corporate legal teams, transactional lawyers |
| Case law research (precedent finding) | Advocates, law students, litigation teams |
| IPC / CrPC section interpretation | Criminal defense lawyers, police, compliance |
| FIR and judgment analysis | Advocates, legal aid organizations |
| Legal notice drafting assistance | Solos and small law firms |
| Regulatory and constitutional research | Policy analysts, compliance officers |

### Key Business Differentiators

- **India-specific**: Integrated with Indian Kanoon API and Indian legal news sources (LiveLaw, Bar and Bench, PRS India), not generic western legal tools.
- **Multi-source answers**: Combines uploaded documents, case law databases, and live web research in a single response.
- **Context retention**: Maintains conversation history so follow-up questions do not require re-explaining context.
- **Fast turnaround**: Built on Groq-hosted Llama 3.3 70B, one of the fastest LLM inference platforms available, keeping response latency low.

---

## Recommended Pricing Model

The following pricing is structured around typical SaaS tiers for legal AI tools in the Indian market, balanced against actual infrastructure and API costs.

### Tier Structure

| Plan | Target Customer | Monthly Price (INR) | Monthly Price (USD ~) |
|---|---|---|---|
| **Starter** | Solo advocate, law student | ₹1,499 / mo | ~$18 |
| **Professional** | Small firm (2–10 lawyers) | ₹5,999 / mo | ~$72 |
| **Business** | Mid-size firm (10–50 lawyers) | ₹14,999 / mo | ~$180 |
| **Enterprise** | Large firm / corporate legal | Custom (₹40,000+) | $480+ |

### What Each Tier Includes

| Feature | Starter | Professional | Business | Enterprise |
|---|---|---|---|---|
| PDF uploads per month | 20 | 100 | 500 | Unlimited |
| Chat queries per month | 200 | 1,000 | 5,000 | Unlimited |
| Max PDF size | 10 MB | 25 MB | 50 MB | 100 MB+ |
| Indian Kanoon searches | 50/mo | 300/mo | 1,500/mo | Unlimited |
| Web research queries | No | Yes | Yes | Yes |
| Chat history retention | 7 days | 30 days | 90 days | 1 year |
| User seats | 1 | 5 | 20 | Custom |
| Priority support | No | Email | Email + Chat | Dedicated |
| Custom integrations / API access | No | No | Yes | Yes |

### Why This Pricing Makes Sense

**Cost to serve one Professional-tier customer/month (estimated):**

| Cost Item | Estimated Monthly Cost |
|---|---|
| Groq API inference (1,000 queries × ~500 tokens each) | ~$1.50–$3.00 |
| Indian Kanoon API calls (300 searches) | ~$3–$6 (depending on plan) |
| Server compute (shared cloud instance fraction) | ~$5–$8 |
| Vector DB storage (Chroma, persistent disk) | ~$1–$2 |
| Total estimated cost | ~$10–$19 / customer |

At ₹5,999/mo (~$72), the gross margin on a Professional customer is roughly **70–80%**, which is standard for B2B SaaS. The Starter tier is deliberately priced near break-even to drive adoption among individual advocates who may graduate to higher tiers.

**Enterprise pricing is negotiated** because large firms require on-premise deployment, SSO, audit logs, and dedicated infrastructure — all of which carry real implementation cost.

---

## Technical Architecture

### System Overview

```
User (Browser)
     │
     ▼
Next.js Frontend (TypeScript, Tailwind CSS, Framer Motion)
     │  REST API calls via Axios
     ▼
Django REST API (Python)
     │
     ▼
Router Agent (LangGraph Orchestrator)
     │
     ├──► Memory Agent       — retrieves previous conversation turns
     ├──► PDF Agent          — queries uploaded document via vector search + LLM
     ├──► Kanoon Agent       — fetches case law from Indian Kanoon API
     ├──► Web Scraper Agent  — scrapes LiveLaw, Bar & Bench, PRS India, etc.
     └──► Drafting Agent     — synthesises all context into final response
                                    │
                                    ▼
                          Groq / Llama 3.3 70B (LLM)
```

### Backend

- **Language**: Python 3.x
- **Framework**: Django 5.1 + Django REST Framework
- **LLM**: Groq API — `llama-3.3-70b-versatile` at temperature 0 (deterministic)
- **Orchestration**: LangChain + LangGraph
- **Vector Database**: ChromaDB (local persistent storage at `legal_db/`)
- **Embeddings**: HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional)
- **PDF Processing**: PyPDF with `RecursiveCharacterTextSplitter` (1,000 char chunks, 200 char overlap)
- **Web Scraping**: BeautifulSoup + requests
- **Production Server**: Gunicorn + WhiteNoise

### Frontend

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4
- **Animations**: Framer Motion
- **UI Primitives**: Radix UI (Dialog)
- **Icons**: Lucide React
- **HTTP**: Axios

### API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/upload/` | Upload a PDF; extracts text, chunks it, stores embeddings in Chroma |
| `POST` | `/api/chat/` | Send a user query; returns AI response with source attribution |

**Upload response:**
```json
{
  "success": true,
  "message": "PDF uploaded successfully.",
  "total_chunks": 42,
  "total_pages": 10,
  "file_name": "contract.pdf"
}
```

**Chat response:**
```json
{
  "success": true,
  "session_id": "uuid",
  "query": "What are the termination clauses?",
  "answer": "..."
}
```

### Routing Logic

The Router Agent (`router_agent.py`) decides which sub-agents to invoke based on query content:

- **Kanoon Agent activates** when the query contains legal keywords: `case`, `judgment`, `section`, `article`, `court`, `bail`, `ipc`, `constitution`, `supreme court`, `high court`, etc.
- **Web Scraper Agent activates** when the query contains temporal keywords: `latest`, `news`, `today`, `recent`, `update` — or contains a URL (`http`, `www`).
- **PDF Agent and Memory Agent** always run for every query.

### Knowledge Sources

1. Uploaded PDFs (via Chroma vector similarity search, top-5 chunks, relevance threshold 0.3)
2. Indian Kanoon API (case law and statutes)
3. Live web: `indiankanoon.org`, `livelaw.in`, `barandbench.com`, `prsindia.org`, Law Commission of India, Constitution India

### Memory

Chat history is maintained per session (UUID-based) in memory, capped at 50 messages. This provides conversational context without requiring a database for early-stage deployments.

---

## Running the Project

### Prerequisites

- Python 3.10+
- Node.js 18+
- `GROQ_API_KEY` from [console.groq.com](https://console.groq.com)
- `KANOON_API_KEY` from Indian Kanoon

### Backend

```bash
cd backend
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_key_here" >> .env
echo "KANOON_API_KEY=your_key_here" >> .env

python manage.py migrate
python manage.py runserver  # Runs on port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev  # Runs on port 3000
```

---

## Current Limitations & Roadmap

| Limitation | Impact | Recommended Fix |
|---|---|---|
| In-memory chat history | Lost on server restart | Persist to PostgreSQL / Redis |
| SQLite database | Not suitable for concurrent production load | Migrate to PostgreSQL |
| CORS allows all origins | Security risk | Restrict to known frontend domains |
| Debug mode enabled | Exposes stack traces | Use environment-based `DEBUG=False` in production |
| No authentication | Anyone with the URL can use the API | Add JWT / OAuth2 |
| Single Chroma instance | No multi-tenancy; all users share a vector space | Namespace collections per user/org |

---

## Target Market & Go-To-Market

**Primary segments:**
1. Individual advocates and solo practitioners (~800,000 enrolled advocates in India)
2. Small and mid-size law firms (top 10,000 firms by revenue)
3. In-house legal departments at mid-market corporates
4. LegalTech-forward law schools and clinics

**Acquisition channels:**
- Bar Council partnerships and legal conference presence
- Content marketing on Indian legal news platforms (LiveLaw, Bar & Bench)
- Direct outreach to law firm managing partners
- Free Starter tier as top-of-funnel

---

## License

Proprietary. All rights reserved. Contact harsh.shukla@raga.ai for licensing inquiries.
