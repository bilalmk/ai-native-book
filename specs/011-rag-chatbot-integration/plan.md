# Implementation Plan: RAG Chatbot Integration

**Branch**: `011-rag-chatbot-integration` | **Date**: 2025-12-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/011-rag-chatbot-integration/spec.md`

## Summary

Build a production-ready RAG (Retrieval-Augmented Generation) chatbot system that integrates with the Docusaurus documentation website. The system enables readers to ask questions about Physical AI & Humanoid Robotics content and receive AI-generated answers with source citations. Technical approach leverages OpenAI embeddings + GPT-4o-mini for generation, Qdrant Cloud for vector search, Neon Postgres for conversation persistence, FastAPI backend, and React/TypeScript frontend integrated via Docusaurus theme swizzling.

## Technical Context

**Language/Version**: Python 3.9+, TypeScript 4.9+, React 18+
**Primary Dependencies**: FastAPI, OpenAI SDK (embeddings + chat), Qdrant client, SQLAlchemy, Pydantic, React, Docusaurus 3+
**Storage**: Qdrant Cloud (vector database for embeddings), Neon Serverless Postgres (relational DB for conversation history)
**Testing**: pytest (backend unit/integration tests), manual testing (frontend E2E via browser)
**Target Platform**: Cloud-hosted FastAPI backend (Railway/Render), GitHub Pages frontend (Docusaurus static site)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: <3s p95 response latency, <50ms vector search, 10 concurrent users, 60fps UI animations
**Constraints**: $15/month budget, free tier services (Qdrant 1GB, Neon 0.5GB), no Docusaurus config changes, 1000 char query limit
**Scale/Scope**: 1000+ documentation pages indexable, 10,000+ vector chunks, 1000 queries/month moderate usage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Required Principles (from constitution.md)

#### ✅ Educational Excellence
- Chatbot answers must be technically accurate, grounded in book content, with clear source citations
- Enhances learning by providing instant clarification without manual search

#### ✅ AI-Native Development
- Leveraging Claude Code + Spec-Kit Plus for feature development
- Using AI (OpenAI GPT-4o-mini) as core component of the learning experience

#### ✅ Spec-Driven Approach
- Feature clearly specified in spec.md with 5 user stories, 48+ functional requirements, success criteria
- Planning follows SDD workflow: spec → plan → tasks → implementation

#### ✅ Innovation & Technology
- Integrates all specified technologies: Docusaurus, OpenAI (Agents/ChatKit concepts), FastAPI, Neon Postgres, Qdrant Cloud
- State-of-the-art RAG pipeline for interactive learning

#### ✅ User-Centric Design
- 5 user stories cover core needs: question answering, context-aware dialogue, text selection, mobile support, loading states
- Accessibility: WCAG AA compliance, keyboard navigation, screen reader support

#### ✅ Maintainability & Scalability
- FastAPI backend (simple, declarative routing)
- OpenAI SDK usage (no heavy customization)
- Modular architecture: indexing, retrieval, generation, conversation management as separate services
- Documentation: architecture.md, quickstart.md, API reference

### RAG Chatbot Governance Compliance

#### ✅ Code Quality & Testing
- Unit tests for vector retrieval, prompt construction, response generation (>80% coverage target)
- Integration tests for end-to-end RAG pipeline
- PEP 8 compliance (automated linters in CI/CD)
- Docstrings + type hints for all functions
- Comprehensive error handling (vector DB failures, LLM API errors, malformed queries)

#### ✅ User Experience Requirements
- Responsive design: desktop (≥1024px), tablet (768-1023px), mobile (≤767px)
- WCAG 2.1 Level AA: keyboard navigation, screen reader compatibility, 4.5:1 color contrast
- Citation display: page/section titles linked to source, visual distinction (footnote-style), zero hallucinated references
- P95 response time ≤2s (requirement: 3s, governance: 2s - will target 2s)
- Clear loading states + graceful degradation messages

#### ✅ Security & Privacy
- No PII storage beyond session management (no names, emails, IP addresses persisted)
- Prompt injection sanitization: input validation, strip system commands, 1000 char limit, malicious pattern detection
- Restricted admin access: environment variables for secrets, no hardcoded API keys
- Rate limiting: 60 queries/hour per IP (to be implemented at infrastructure level if needed)
- Data encryption: HTTPS for all communication, encrypted config at rest

#### ✅ Performance Expectations
- Asynchronous design: FastAPI with asyncio, async/await for all I/O operations
- No blocking calls: async HTTP clients (httpx), async DB drivers (asyncpg)
- Latency monitoring: instrument retrieval time, generation time, total response time
- Resource limits: max 10 concurrent LLM API calls, connection pooling for Postgres/Qdrant
- Caching strategy: cache frequent queries (TTL 1 hour)

#### ✅ RAG & Citation Discipline
- Grounded answers: all responses must be based on textbook content
- Source attribution: every factual claim cites specific page/section
- No hallucination: confidence threshold (similarity score <0.7 triggers "insufficient information" response)
- Context window management: top 5 relevant chunks, ≤2000 tokens total
- Citation validation: periodic audits to verify accuracy

#### ✅ Maintainability Standards
- Framework discipline: FastAPI for backend, no unnecessary abstractions
- OpenAI SDK usage: follow best practices, rely on official APIs
- Architecture documentation: docs/rag-architecture.md with system diagram, data flow, deployment topology
- Quick-start guide: docs/rag-quickstart.md with local dev setup, testing, deployment
- Dependency management: pin exact versions (requirements.txt or pyproject.toml)
- Code reviews: all changes require peer review for adherence to principles

### Gates Status: ✅ ALL PASSED

No violations detected. Feature aligns with all constitution principles and RAG governance requirements.

## Project Structure

### Documentation (this feature)

```text
specs/011-rag-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── api-spec.yaml   # OpenAPI specification for REST endpoints
│   ├── database-schema.sql  # Postgres schema definitions
│   └── qdrant-schema.json   # Qdrant collection configuration
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Environment variables, settings
│   ├── models/
│   │   ├── chat.py            # Pydantic models (ChatMessage, ChatSession)
│   │   └── document.py        # Pydantic models (DocumentChunk, Source)
│   ├── services/
│   │   ├── embedding.py       # OpenAI embeddings service
│   │   ├── vector_store.py    # Qdrant vector database operations
│   │   ├── llm.py             # OpenAI chat completion service
│   │   ├── conversation.py    # Postgres conversation persistence
│   │   └── indexing.py        # Document chunking and indexing
│   ├── api/
│   │   ├── health.py          # GET /api/health endpoint
│   │   ├── chat.py            # POST /api/chat endpoint
│   │   └── sessions.py        # GET /api/sessions/{id}/history endpoint
│   └── utils/
│       ├── markdown.py        # Markdown parsing and cleaning
│       └── sanitization.py    # Input validation and prompt injection prevention
├── tests/
│   ├── unit/
│   │   ├── test_embedding.py
│   │   ├── test_vector_store.py
│   │   ├── test_llm.py
│   │   ├── test_conversation.py
│   │   └── test_sanitization.py
│   └── integration/
│       ├── test_rag_pipeline.py
│       └── test_api_endpoints.py
├── scripts/
│   └── index_docs.py          # Script to index documentation files
├── pyproject.toml             # UV package manager configuration
├── requirements.txt           # Python dependencies (pinned versions)
└── .env.example               # Environment variable template

frontend/
├── src/
│   └── theme/
│       ├── Root.tsx           # Docusaurus swizzled root component
│       └── components/
│           ├── ChatWidget/
│           │   ├── index.tsx          # Main chat widget component
│           │   ├── ChatButton.tsx     # Floating chat button
│           │   ├── ChatWindow.tsx     # Chat window container
│           │   ├── MessageList.tsx    # Message rendering
│           │   ├── InputArea.tsx      # User input field
│           │   ├── SourceCitation.tsx # Citation display
│           │   ├── TextSelection.tsx  # Selected text banner
│           │   └── styles.module.css  # Component styles
│           └── api/
│               └── chatApi.ts         # API client for backend
└── tsconfig.json              # TypeScript configuration

docs/
├── rag-architecture.md        # System architecture documentation
└── rag-quickstart.md          # Setup and deployment guide
```

**Structure Decision**: Web application structure with backend (Python/FastAPI) and frontend (React/TypeScript) integration. Backend is a standalone FastAPI service deployable to cloud platforms. Frontend integrates into existing Docusaurus site via theme swizzling (non-invasive approach that doesn't modify docusaurus.config.js). Documentation files stored at root `docs/` level for easy access.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. This section intentionally left empty.

---

## Phase 0: Outline & Research

**Status**: PENDING
**Output**: `research.md`

### Research Tasks

1. **OpenAI Embeddings Best Practices**
   - Research: text-embedding-3-small model specifications (dimension: 1536, cost per token)
   - Research: Optimal chunk size for embeddings (balancing context vs. granularity)
   - Research: Batch embedding strategies to reduce API calls
   - Decision: Chunk size, overlap strategy, batch size

2. **RAG Pipeline Patterns**
   - Research: Industry best practices for RAG pipelines (retrieval, reranking, generation)
   - Research: Context window management for GPT-4o-mini (max tokens, optimal context length)
   - Research: Prompt engineering for grounded responses (system prompts, few-shot examples)
   - Decision: Prompt template, context inclusion strategy, confidence thresholds

3. **Qdrant Cloud Integration**
   - Research: Qdrant free tier limitations (1GB storage, request limits)
   - Research: Collection configuration (distance metric: cosine vs. dot product)
   - Research: Search strategies (similarity search, filtering by metadata)
   - Decision: Collection setup, indexing strategy, search parameters

4. **Neon Serverless Postgres Patterns**
   - Research: Neon free tier limitations (0.5GB storage, connection pooling)
   - Research: Async database drivers for FastAPI (asyncpg vs. psycopg3)
   - Research: Session management patterns (session expiration, cleanup strategies)
   - Decision: Database schema, connection pooling, session lifecycle

5. **Docusaurus Theme Swizzling**
   - Research: Safe swizzling patterns (Root component, global integration)
   - Research: Theme compatibility (light/dark mode, responsive design)
   - Research: Performance implications (lazy loading, code splitting)
   - Decision: Swizzling approach, component lifecycle, styling strategy

6. **Prompt Injection Prevention**
   - Research: Common prompt injection attacks in RAG systems
   - Research: Input sanitization techniques (pattern detection, validation rules)
   - Research: LLM safety best practices (system prompts, output validation)
   - Decision: Sanitization rules, validation patterns, error handling

7. **Accessibility Standards (WCAG AA)**
   - Research: Keyboard navigation patterns for chat widgets
   - Research: ARIA labels for screen readers in conversational UIs
   - Research: Color contrast requirements (4.5:1 for normal text)
   - Decision: Accessibility implementation checklist, testing approach

8. **Frontend Performance Optimization**
   - Research: React optimization patterns (memo, lazy loading, virtualization)
   - Research: Animation performance (CSS transforms, 60fps targets)
   - Research: Bundle size optimization (tree shaking, code splitting)
   - Decision: Performance budget, optimization techniques

### Consolidation Format (research.md)

For each research area above:
- **Decision**: [Final choice]
- **Rationale**: [Why this approach was selected]
- **Alternatives Considered**: [Other options evaluated and why rejected]
- **References**: [Links to documentation, articles, benchmarks]

---

## Phase 1: Design & Contracts

**Status**: PENDING
**Prerequisites**: `research.md` complete
**Output**: `data-model.md`, `contracts/*`, `quickstart.md`, updated agent context

### Data Model (data-model.md)

**Entities to Extract from Spec**:

1. **ChatSession**
   - Fields: session_id (UUID, PK), created_at (timestamp), last_activity_at (timestamp)
   - Relationships: has many ChatMessage
   - Validation: session_id must be valid UUID, timestamps in ISO 8601 format
   - State Transitions: created → active → expired (after 7 days inactivity)

2. **ChatMessage**
   - Fields: message_id (UUID, PK), session_id (UUID, FK), role (enum: user/assistant), content (text), selected_text (text, nullable), context_used (JSON, nullable), created_at (timestamp)
   - Relationships: belongs to ChatSession
   - Validation: role must be 'user' or 'assistant', content length 1-10000 chars, selected_text length 1-1000 chars
   - State Transitions: N/A (immutable once created)

3. **DocumentChunk** (Qdrant vector database)
   - Fields: chunk_id (UUID), title (text), file_path (text), chunk_text (text), chunk_index (int), total_chunks (int), embedding (vector[1536]), metadata (JSON)
   - Relationships: N/A (stored in vector database)
   - Validation: embedding dimension must be 1536, chunk_index >= 0, total_chunks > 0
   - State Transitions: indexed → active → updated (on doc changes)

4. **Source** (ephemeral, not persisted)
   - Fields: title (text), file_path (text), relevance_score (float 0-1), excerpt (text)
   - Relationships: derived from DocumentChunk during retrieval
   - Validation: relevance_score between 0 and 1, excerpt length < 500 chars

### API Contracts (contracts/)

**Endpoints to Generate**:

1. **GET /api/health**
   - Response: `{status: "healthy", services: {qdrant: "up", postgres: "up", openai: "up"}}`
   - Status Codes: 200 (all healthy), 503 (service unavailable)

2. **POST /api/chat**
   - Request: `{message: string, session_id?: string, selected_text?: string}`
   - Response: `{session_id: string, message: string, sources: Source[], timestamp: string}`
   - Status Codes: 200 (success), 400 (invalid input), 429 (rate limit), 500 (server error)

3. **GET /api/sessions/{session_id}/history**
   - Response: `{session_id: string, messages: ChatMessage[]}`
   - Status Codes: 200 (success), 404 (session not found), 500 (server error)

**Output Files**:
- `contracts/api-spec.yaml`: OpenAPI 3.0 specification
- `contracts/database-schema.sql`: Postgres CREATE TABLE statements
- `contracts/qdrant-schema.json`: Qdrant collection configuration

### Quick Start Guide (quickstart.md)

**Structure**:
1. Prerequisites (Python 3.9+, Node.js 18+, external service signups)
2. Backend Setup (clone, install dependencies via UV, configure .env, initialize databases)
3. Frontend Integration (install dependencies, swizzle Root component, configure API URL)
4. Running Locally (start backend, start Docusaurus dev server, test chat)
5. Testing (run unit tests, run integration tests, manual testing checklist)
6. Deployment (deploy backend to Railway/Render, deploy frontend to GitHub Pages, configure CORS)
7. Troubleshooting (common errors and solutions)

### Agent Context Update

**Command**: Run `.specify/scripts/bash/update-agent-context.sh claude`

**Expected Updates** (to `.claude/agents/rag_agent.md` or similar):
- Add: "RAG Chatbot Integration (011-rag-chatbot-integration)"
- Technologies: FastAPI, OpenAI SDK, Qdrant Cloud, Neon Postgres, React/TypeScript
- Context: Available for RAG-related tasks (embeddings, vector search, conversation management)

---

## Phase 2: Task Generation

**Status**: OUT OF SCOPE FOR /sp.plan
**Next Step**: User runs `/sp.tasks` command to generate `tasks.md`

The `/sp.plan` command ends here. Task generation is handled by a separate command (`/sp.tasks`) that consumes the outputs from this plan (research.md, data-model.md, contracts/, quickstart.md).

---

## Follow-Up Actions

After this plan is complete:
1. Review `research.md` to validate all technical decisions
2. Review `data-model.md` to ensure entities align with spec requirements
3. Review `contracts/` to verify API specifications are complete
4. Review `quickstart.md` to ensure setup is reproducible
5. Run `/sp.tasks` to generate implementation tasks
6. Consider ADR for significant architectural decisions:
   - ADR candidate: "RAG Pipeline Architecture (OpenAI + Qdrant + GPT-4o-mini)"
   - ADR candidate: "Docusaurus Integration via Theme Swizzling"
   - ADR candidate: "Session Management Strategy (7-day expiration)"

---

## Notes

- User input mentioned: "you can use rag_agent for rag relate things, frontend-design skills for frontend designing and rag_skills for rag related things"
- These agents/skills will be leveraged during implementation phase (`/sp.implement`)
- This plan focuses on design and contracts; implementation execution is out of scope
