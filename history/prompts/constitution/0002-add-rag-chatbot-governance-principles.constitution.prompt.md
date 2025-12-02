---
id: 0002
title: Add RAG Chatbot Governance Principles
stage: constitution
date: 2025-12-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: system
command: /sp.constitution
labels: ["constitution", "rag-chatbot", "governance", "testing", "security", "performance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (documentation update)
---

## Prompt

```text
Update our Physical AI & Humanoid Robotics textbook constitution by adding governing principles for the integrated RAG chatbot. Keep the existing vision, target audience, AI-native development approach and educational principles intact. Append new sections covering:

• Code quality and testing (unit and integration tests, PEP 8 compliance, documented functions).
• User‑experience requirements for the chat widget (responsive, accessible, clearly displays citations, ≤2 s response time).
• Security and privacy guidelines (no PII storage, prompt‑injection sanitisation, restricted admin access).
• Performance expectations (asynchronous design, monitored latency, no blocking calls).
• RAG & citation discipline (answers must be grounded in the book, clearly cite source pages).
• Maintainability (use FastAPI and ChatKit judiciously, document architecture and provide a quick‑start guide).

Also update the version number and amendment date accordingly.
```

## Response snapshot

Updated constitution from version 1.0.0 → 1.1.0 with comprehensive RAG Chatbot Governance section including:

**New Sections Added:**
1. **Code Quality & Testing**: Mandates >80% test coverage, PEP 8 compliance, comprehensive error handling, type hints, and docstrings for all functions.

2. **User Experience Requirements**: Enforces responsive design (desktop/tablet/mobile), WCAG 2.1 Level AA accessibility, clear citation display with source links, P95 response time ≤2s, and loading state indicators.

3. **Security & Privacy**: Prohibits PII storage, requires prompt injection sanitization, restricted admin access with API key authentication, per-IP rate limiting (60/hour), and HTTPS encryption.

4. **Performance Expectations**: Mandates async/await patterns for all I/O operations, prohibits blocking calls, requires latency monitoring with P95/P99 thresholds, connection pooling, and query caching (TTL 1 hour).

5. **RAG & Citation Discipline**: Requires all responses grounded in textbook content, 100% accurate citations, confidence thresholds (≥0.7 similarity score), limited context (top 5 chunks, ≤2000 tokens), and periodic citation audits.

6. **Maintainability Standards**: Enforces FastAPI best practices, OpenAI ChatKit SDK usage without heavy customization, comprehensive architecture documentation (`docs/rag-architecture.md`), quick-start guide, pinned dependencies, and mandatory code reviews.

**Enhanced Success Metrics:**
- Accuracy: >90% responses grounded in content
- Citation Precision: 100% (zero hallucinations)
- Response Latency: P95 ≤2s, P99 ≤3s
- User Satisfaction: >4.0/5.0
- Uptime: 99.5%
- Security: Zero PII leakage or prompt injection incidents
- Code Quality: >80% test coverage, PEP 8 compliance, zero critical vulnerabilities

**Version Bump Rationale:**
MINOR version (1.0.0 → 1.1.0) because new governance sections were added without removing or breaking existing principles. This is an additive change that materially expands project guidance.

## Outcome

- ✅ Impact: Constitution successfully updated with comprehensive RAG chatbot governance principles. Version incremented to 1.1.0. All existing vision, principles, and structure preserved.
- 🧪 Tests: N/A (documentation update; no code changes)
- 📁 Files: Updated `.specify/memory/constitution.md` with new RAG Chatbot Governance section (6 subsections + enhanced metrics)
- 🔁 Next prompts: Consider documenting RAG architecture decisions with `/sp.adr` for significant technical choices (vector DB selection, embedding model, retrieval strategy, LLM provider)
- 🧠 Reflection: The constitution now provides clear, testable governance for RAG chatbot development. Each principle includes explicit rationale and measurable requirements. Templates (plan, spec, tasks) already include Constitution Check sections that will naturally incorporate these new principles.

## Evaluation notes (flywheel)

- Failure modes observed: None. Constitution update was straightforward; existing templates already structured for constitution compliance checks.
- Graders run and results (PASS/FAIL): Manual validation PASS - no unresolved placeholders, version/dates updated correctly, new sections properly formatted with rationale.
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Monitor whether the new RAG governance principles surface effectively during `/sp.plan` and `/sp.tasks` execution for RAG-related features. Validate that Constitution Check gates catch violations of RAG principles.
