# 🧠 LLM-Powered Document Processing and Analysis Platform

A scalable, modular AI platform that ingests, analyzes, and extracts structured insights from unstructured documents using Large Language Models (LLMs) combined with Retrieval-Augmented Generation (RAG). This system is built to automate enterprise-level document understanding and accelerate decision-making workflows.

---

## 📌 Key Features

- 📄 **Multi-format Ingestion**: Supports PDF, DOCX, TXT, and scanned image documents with OCR.
- 🔍 **Advanced RAG Pipeline**: Combines semantic retrieval with LLM generation for context-aware extraction.
- 🧠 **Named Entity Recognition (NER)**: Extracts people, organizations, dates, and domain-specific entities.
- 🔗 **Relationship Mapping**: Builds relationship graphs between entities for deeper insights.
- 🧾 **Summarization**: Generates layered summaries from detailed to concise.
- 💬 **Natural Language Q&A**: Enables conversational queries over document content.
- 🔐 **JWT Authentication**: Secures API access.
- 📊 **Monitoring & MLOps**: Integrates with Prometheus and MLflow for tracking and observability.

---

## 🏗️ Project Structure
llm-doc-platform/
├── api/                 # FastAPI routes and endpoints
├── analysis/            # NLP modules: NER, summarizer, relationship mapping, etc.
├── auth/                # JWT authentication and user models
├── ingestion/           # Document and metadata extraction
├── monitoring/          # Prometheus and MLflow setup
├── nlp/                 # Natural language query handler
├── rag/                 # RAG retriever logic and embedding generation
├── frontend/            # (Planned) React + D3.js UI components
├── prometheus.yml       # Prometheus configuration
└── requirements.txt     # Python dependencies
---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/llm-doc-platform.git
cd llm-doc-platform
2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Set Environment Variables

Create a .env file in the root directory:
OPENAI_API_KEY=your_api_key_here
JWT_SECRET_KEY=your_jwt_secret