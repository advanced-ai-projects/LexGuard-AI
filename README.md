# LexGuard AI

**Production-Grade, Compliant Legal RAG System on AWS**

---

## Overview

**LexGuard AI** is a production-grade legal assistant built on **AWS** that delivers **accurate, citation-backed, and auditable answers** from trusted legal sources using **retrieval-augmented generation (RAG)** and **controlled agentic workflows**.

Designed for real-world legal scrutiny, LexGuard AI prioritizes:

- Citation integrity  
- Explainability  
- Auditability  
- GDPR-aligned responsible AI  
- Production reliability (latency, cost, monitoring)

This project demonstrates how to move from **LLM experimentation to stable, compliant legal AI APIs**.

---

## Problem Statement

Legal professionals cannot rely on AI systems that:

- Hallucinate legal facts  
- Fail to cite sources  
- Cannot explain reasoning  
- Lack audit trails  
- Ignore privacy and regulatory obligations  

At the same time, purely manual legal research is slow, costly, and inconsistent.

---

## Solution

LexGuard AI provides a **compliance-first legal AI architecture** that:

- Retrieves answers only from **trusted legal sources**
- Enforces **citation grounding**
- Applies **safe refusals** when confidence is low
- Maintains **full audit trails**
- Operates as a **production-ready API**

---

## Core Capabilities

### 1. Legal Document Ingestion

- Ingests trusted legal content such as:
  - GOV.UK guidance
  - ACAS employment law resources
  - Statutory instruments (sample data)
- Section-aware parsing:
  - Acts
  - Sections
  - Subsections
- Rich metadata:
  - Jurisdiction
  - Source
  - Publication date
  - Legal domain

---

### 2. Retrieval-Augmented Generation (RAG)

- Hybrid retrieval:
  - Keyword search (BM25)
  - Vector similarity search
- Advanced chunking strategies
- Metadata-aware filtering
- Re-ranking for legal relevance

---

### 3. Citation Integrity & Grounding

Every response:
- Is grounded in retrieved legal sources
- Includes inline citations
- References:
  - Document name
  - Section / paragraph
  - Source URL (where applicable)

If no reliable source is found:
- The system **refuses safely**
- Explains the limitation transparently

---

### 4. Agentic Legal Reasoning (Controlled)

LexGuard AI uses a **deterministic, auditable agentic workflow**:

1. Interpret user query
2. Rewrite query for retrieval
3. Retrieve relevant legal sources
4. Re-rank results
5. Generate answer
6. Validate citation coverage
7. Respond or refuse

This avoids uncontrolled autonomous agents while retaining multi-step reasoning.

---

### 5. Evaluation & Quality Gates

Built-in evaluation includes:

- Golden legal Q&A datasets
- Regression testing on every change
- Citation coverage checks
- Safety and refusal correctness checks

No change is released without passing quality gates.

---

### 6. Stable Production APIs

- REST API with:
  - Clear request/response contracts
  - Versioning
  - Rate-limit-ready design
- Authentication-ready (OAuth-compatible)
- Predictable latency and cost behavior

---

### 7. Responsible AI & GDPR by Design

- Privacy-first prompts
- No PII persistence
- Safe refusals for unsupported queries
- Audit logs for:
  - Queries
  - Retrieved sources
  - Generated responses
- Data minimization and retention controls

---

## AWS-Native Architecture

### Core AWS Services

| Capability | AWS Service |
|----------|-------------|
| LLMs | Amazon Bedrock (Claude) |
| Vector Search | Amazon OpenSearch (Vector Engine) |
| Storage | Amazon S3 |
| Compute | AWS Lambda or ECS |
| Secrets | AWS Secrets Manager |
| Monitoring | CloudWatch |
| Tracing | AWS X-Ray |

---

### Architecture Flow

User Query
|
v
API Layer (FastAPI)
|
v
Query Rewriter (LLM)
|
v
Hybrid Retrieval (OpenSearch)
|
v
Re-ranker
|
v
Answer Generator (Bedrock)
|
v
Citation Validator
|
+--> Answer with citations
|
+--> Safe refusal

yaml
Copy code

---

## Repository Structure

lexguard-ai/

├── ingestion/

│ ├── loaders.py

│ ├── chunking.py

│ ├── metadata.py

│

├── retrieval/
│ ├── hybrid_search.py
│ ├── reranker.py
│
├── agents/
│ ├── legal_agent.py
│ ├── query_rewrite.py
│
├── evaluation/
│ ├── golden_set.json
│ ├── regression_tests.py
│
├── compliance/
│ ├── safe_refusal.py
│ ├── audit_log.py
│
├── api/
│ ├── main.py
│
├── infra/
│ ├── aws_architecture.md
│
├── README.md

yaml
Copy code

---

## Evaluation Strategy

LexGuard AI evaluates:

- Accuracy
- Citation completeness
- Refusal correctness
- Latency
- Cost per request

Evaluation methods:
- Golden test cases
- Automated regression tests
- Manual spot checks
- Confidence threshold validation

---

## Security & Compliance

- No sensitive data stored in logs
- Deterministic retrieval and decision paths
- Full traceability for audits
- Designed for GDPR and responsible AI compliance
- Supports legal review and incident investigation

---

## Optional Enhancements (Only If You Want to Go Further)

These features are **not required**, but demonstrate advanced maturity and production thinking.

---

### 1️⃣ Streamlit Review UI

A lightweight Streamlit app to:
- Submit legal questions
- View retrieved sources
- Inspect citations
- Review refusals and confidence scores

Purpose:
- Human review
- Demo for stakeholders
- Legal validation

---

### 2️⃣ Cost Tracking Per Request

- Track token usage per request
- Estimate LLM cost per response
- Log cost metrics to CloudWatch

Purpose:
- Cost transparency
- Budget control
- Production tuning

---

### 3️⃣ Jurisdiction Filtering

- Filter retrieval by jurisdiction:
  - UK
  - EU
  - Other regions (extensible)
- Enforced at retrieval and generation time

Purpose:
- Prevent cross-jurisdiction legal errors
- Improve relevance and compliance

---

### 4️⃣ Document Freshness Scoring

- Weight newer legal documents higher
- Penalize outdated guidance
- Include publication date in ranking logic

Purpose:
- Ensure up-to-date legal advice
- Reduce reliance on superseded law

---

## Roadmap

Planned future work:
- Policy versioning
- Model drift detection
- Expanded legal sources
- Multi-tenant deployment
- Advanced monitoring dashboards

---

## Why This Project Matters

LexGuard AI demonstrates:

- Production-grade legal AI engineering
- Trustworthy RAG design
- Responsible, auditable AI systems
- AWS-native deployment
- Evaluation-driven development

This project reflects **real-world legal AI constraints**, not experimental prototypes.

---

## Author

**John Z. Arufandika**  
AI Engineer | Digital Transformation | Legal & Regulated AI Systems

---

## License

This project is provided for portfolio and educational purposes.
