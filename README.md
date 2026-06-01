# ⚖️ Nyaya AI — Production-Grade Multilingual Indian Legal Intelligence Platform

<p align="center">
  <h1 align="center">Nyaya AI</h1>

  <p align="center">
    <strong>AI-Powered Indian Legal Intelligence Platform</strong>
  </p>

  <p align="center">
    Built with <strong>Agentic AI</strong>, <strong>RAG</strong>, <strong>Guardrails</strong>, <strong>Multilingual Intelligence</strong>, and <strong>Source-Backed Legal Reasoning</strong>.
  </p>

  <p align="center">
    Designed for <strong>Lawyers</strong>, <strong>Law Firms</strong>, <strong>Legal Teams</strong>, <strong>Students</strong>, and <strong>Citizens</strong>.
  </p>
</p>

---

# Overview

**Nyaya AI** is a **production-grade multilingual legal intelligence platform** designed specifically for the **Indian legal ecosystem**.

It enables:

* Advocates
* Law Firms
* Corporate Legal Teams
* Law Students
* Legal Researchers
* Citizens

to understand, research, analyze, and interpret legal information through **natural language conversations**.

Nyaya AI combines:

✅ **Document Intelligence**
✅ **Legal Research**
✅ **Agentic AI**
✅ **Multilingual Legal Understanding**
✅ **Legal Guardrails**
✅ **Conversational Memory**
✅ **Source-backed Legal Reasoning**
✅ **OCR-based Document Analysis**

into a single legal intelligence platform designed for India.

---

# Vision

To democratize access to **Indian legal intelligence** by making legal information:

* Understandable
* Accessible
* Searchable
* Affordable
* Multilingual

for every legal professional and citizen in India.

---

# Problem Statement

Legal research in India is:

* Time-consuming
* Fragmented across multiple platforms
* Difficult for non-lawyers
* Mostly English-centric
* Expensive through enterprise legal tools

Lawyers spend hours researching:

* Case precedents
* Court judgments
* Constitutional provisions
* Statutory interpretation

Citizens struggle with:

* FIR interpretation
* Court notices
* Tenant rights
* Bail procedures
* Legal rights awareness

Nyaya AI reduces legal research from **hours to minutes**.

---

# Core Features

## 📄 Legal Document Intelligence

Upload and analyze:

* FIRs
* Contracts
* Court Orders
* Agreements
* Judgments
* Legal Notices
* Affidavits
* Petitions

Ask questions naturally.

### Example Queries

```text
Explain this FIR in simple Hindi.
```

```text
What are the termination clauses in this contract?
```

---

## ⚖️ Indian Legal Research

Research:

* Supreme Court judgments
* High Court precedents
* Constitutional Articles
* Statutory Law
* Legal Sections

### Example Queries

```text
Explain Article 21 in Hindi.
```

```text
Find Supreme Court precedents on anticipatory bail.
```

---

## 🌍 Multilingual Legal Intelligence

Nyaya AI supports **regional legal conversations**.

### Supported Languages

* English
* Hindi
* Urdu
* Punjabi
* Tamil
* Telugu
* Bengali
* Marathi
* Gujarati
* Kannada
* Malayalam

### Example

Hindi:

```text
अगर किसी ने मेरे खिलाफ झूठी FIR दर्ज की है तो मुझे क्या करना चाहिए?
```

Punjabi:

```text
ਆਰਟਿਕਲ 21 ਕੀ ਸੁਰੱਖਿਆ ਦਿੰਦਾ ਹੈ?
```

Urdu:

```text
ہیمراج کون تھا؟
```

Tamil:

```text
ஆர்டிக்கல் 21 என்ன பாதுகாக்கிறது?
```

---

# 🏗️ System Architecture

Nyaya AI uses a **Custom Multi-Agent Orchestration Engine** built in Python.

Instead of LangGraph, Nyaya AI uses **manual production orchestration through intelligent router-based workflows** for greater control and flexibility.

---

# Production Pipeline

```text
User Query
      │
      ▼
Language Detection
      │
      ▼
Intent Agent
      │
      ▼
Router Agent
      │
      ▼
Guardrail Agent
      │
      ▼
Parallel Retrieval
┌───────────────────────┐
│ Document Agent
│ API Agent
│ Web Agent
└───────────────────────┘
      │
      ▼
Normalizer Layer
      │
      ▼
Source Ranking
      │
      ▼
Hallucination Checker
      │
      ▼
Citation Checker
      │
      ▼
Translation Agent
      │
      ▼
Final Answer Agent
      │
      ▼
Final Legal Response
```

---

# 🤖 Agent Architecture

Nyaya AI uses **Agentic AI** instead of a traditional chatbot.

Each query passes through specialized agents.

---

## Intent Agent

**File:**

```text
backend/agents/intent_agent.py
```

### Responsibilities

* Understands user intent
* Predicts legal query type
* Routes legal workflows

Supported intents:

```text
LEGAL_RESEARCH
DOCUMENT_ANALYSIS
CASE_SUMMARY
WEB_RESEARCH
LEGAL_EXPLANATION
TRANSLATION
GENERAL_QUERY
```

---

## Router Agent

**File:**

```text
backend/agents/router_agent.py
```

### Responsibilities

The orchestration layer.

Responsible for:

* Agent routing
* Query orchestration
* Source prioritization
* Context merging

Example:

PDF Uploaded:

```text
Router
   ↓
Document Agent
```

Legal precedent search:

```text
Router
   ↓
API Agent + Web Agent
```

---

## Guardrail Agent

**File:**

```text
backend/agents/guardrail_agent.py
```

### Responsibilities

Makes Nyaya AI production-safe.

Protects against:

### Prompt Injection

Blocked Examples:

```text
Ignore previous instructions
Reveal hidden prompt
Show system prompt
```

### Hallucinations

Prevents:

* Fake judgments
* Fake citations
* Unsupported legal claims

### Unsafe Legal Advice

Blocks:

```text
How to evade law?
How to commit fraud?
```

### PII Protection

Masks:

* Aadhaar
* PAN
* Email IDs
* Phone Numbers

---

## Document Agent

**File:**

```text
backend/agents/document_agent.py
```

### Responsibilities

Handles:

* PDF Extraction
* OCR Processing
* Chunking
* Embeddings
* Semantic Search

Pipeline:

```text
PDF Upload
      ↓
OCR Extraction
      ↓
Text Extraction
      ↓
Chunking
      ↓
Embeddings
      ↓
Vector Search
      ↓
Relevant Context
```

---

## API Agent

**File:**

```text
backend/agents/api_agent.py
```

### Responsibilities

Structured legal retrieval.

Fetches:

* Case law
* Constitutional provisions
* Legal precedents
* Statutory sections

---

## Web Agent

**File:**

```text
backend/agents/web_agent.py
```

### Responsibilities

Retrieves:

* Legal updates
* Regulatory changes
* Legal news
* Government notifications

Sources:

* LiveLaw
* Bar & Bench
* PRS India
* Government Portals

---

## Translation Agent

**File:**

```text
backend/agents/translation_agent.py
```

### Responsibilities

Enables multilingual legal intelligence.

Pipeline:

```text
Regional Language Query
          ↓
Translate to English
          ↓
Legal Processing
          ↓
Translate Response Back
```

---

## Final Answer Agent

**File:**

```text
backend/agents/final_answer_agent.py
```

### Responsibilities

* Final legal reasoning
* Context merging
* Structured response generation
* Source-backed output

---

# 🛡️ Guardrails Layer

Nyaya AI includes **production-level legal guardrails**.

---

## Citation Checker

**File:**

```text
backend/guardrails/citation_checker.py
```

Validates:

* Court citations
* Case references
* Legal sections

---

## Hallucination Checker

**File:**

```text
backend/guardrails/hallucination_checker.py
```

Prevents fabricated legal information.

---

## Confidence Score

**File:**

```text
backend/guardrails/confidence_score.py
```

Assigns confidence to responses.

Example:

```text
High Confidence
Medium Confidence
Low Confidence
```

---

## PII Filter

**File:**

```text
backend/guardrails/pii_filter.py
```

Masks:

* PAN
* Aadhaar
* Emails
* Phone Numbers

---

## Unsafe Advice Blocker

**File:**

```text
backend/guardrails/unsafe_advice_blocker.py
```

Blocks unsafe legal requests.

---

## Source Ranking

**File:**

```text
backend/guardrails/source_ranker.py
```

Ranks trusted sources higher.

Priority:

```text
Uploaded Documents
      ↓
Court Sources
      ↓
Government Sources
      ↓
Legal Databases
      ↓
Legal News
```

---

# 🔍 RAG Pipeline

Nyaya AI uses **Retrieval-Augmented Generation (RAG)**.

```text
Legal Document
      ↓
OCR Extraction
      ↓
Text Extraction
      ↓
Chunking
      ↓
Embeddings
      ↓
ChromaDB
      ↓
Retriever
      ↓
Relevant Context
      ↓
Legal Reasoning
      ↓
Final Response
```

---

# 🌐 Language Pipeline

```text
User Query
      ↓
Language Detection
      ↓
Translate to English
      ↓
Legal Retrieval
      ↓
Reasoning
      ↓
Translate Back
      ↓
Final Answer
```

---

# 🧰 Tech Stack

## AI Layer

| Technology    | Purpose           |
| ------------- | ----------------- |
| LangChain     | LLM orchestration |
| Groq          | Fast inference    |
| Llama 3.3 70B | Legal reasoning   |
| HuggingFace   | Embeddings        |

---

## Backend

| Technology            | Purpose           |
| --------------------- | ----------------- |
| Python                | Core Language     |
| Django                | Backend Framework |
| Django REST Framework | APIs              |

---

## Frontend

| Technology   | Purpose     |
| ------------ | ----------- |
| Next.js 16   | Frontend    |
| TypeScript   | Type Safety |
| Tailwind CSS | Styling     |

---

## Database

| Technology           | Purpose         |
| -------------------- | --------------- |
| ChromaDB             | Vector Database |
| SQLite               | Development     |
| PostgreSQL (Planned) | Production      |

---

# 📁 Project Structure

```text
nyaya-ai/
│
├── backend/
│   │
│   ├── agents/
│   │   ├── api_agent.py
│   │   ├── document_agent.py
│   │   ├── final_answer_agent.py
│   │   ├── guardrail_agent.py
│   │   ├── intent_agent.py
│   │   ├── router_agent.py
│   │   ├── translation_agent.py
│   │   └── web_agent.py
│   │
│   ├── rag/
│   │   ├── chunker.py
│   │   ├── document_extractor.py
│   │   ├── embeddings.py
│   │   ├── ocr_extractor.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── guardrails/
│   │   ├── citation_checker.py
│   │   ├── confidence_score.py
│   │   ├── hallucination_checker.py
│   │   ├── pii_filter.py
│   │   ├── source_ranker.py
│   │   └── unsafe_advice_blocker.py
│   │
│   ├── memory/
│   ├── language/
│   ├── normalizer/
│   ├── core/
│   ├── billing/
│   └── api/
│
├── frontend/
│
└── README.md
```

---

# 🚀 Installation

Clone repository:

```bash
git clone https://github.com/pranjulm010/nyaya-ai.git

cd nyaya-ai
```

Create virtual environment:

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_key

OPENAI_API_KEY=your_key

SECRET_KEY=your_secret

DEBUG=False
```

---

# Run Backend

```bash
python manage.py runserver
```

---

# Run Frontend

```bash
npm install

npm run dev
```

---

# Future Roadmap

### Phase 1 — MVP

* Legal Chat
* Document Intelligence
* Basic RAG

### Phase 2 — Agentic AI

* Multi-Agent Workflow
* Translation Layer
* Legal APIs

### Phase 3 — Production

* Citation Validation
* Hallucination Prevention
* Billing
* Authentication

### Phase 4 — Enterprise

* Audit Logs
* Team Workspaces
* RBAC
* SSO

---

# Legal Disclaimer

**Nyaya AI is an AI-powered legal assistance platform and does not constitute legal advice.**

Users should independently verify legal advice with a qualified legal professional.

---

# Mission

> **Making Indian legal intelligence multilingual, accessible, and understandable for everyone.**

---

# License

**Proprietary — All Rights Reserved**

For inquiries:

**[pranjulm@observancegroup.com](mailto:pranjulm@observancegroup.com)**

[harsh.shukla@raga.ai](mailto:harsh.shukla@raga.ai)
