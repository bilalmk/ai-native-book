<!-- Sync Impact Report:
Version change: 1.0.0 → 1.1.0
Modified principles:
  - None (existing principles preserved)
Added sections:
  - RAG Chatbot Governance (7 new subsections)
    - Code Quality & Testing
    - User Experience Requirements
    - Security & Privacy
    - Performance Expectations
    - RAG & Citation Discipline
    - Maintainability Standards
  - Updated Success Metrics to include RAG chatbot specific metrics
Modified sections:
  - Success Metrics: Enhanced with RAG-specific performance indicators
Removed sections:
  - None
Templates requiring updates:
  - .specify/templates/plan-template.md (✅ updated)
  - .specify/templates/spec-template.md (✅ updated)
  - .specify/templates/tasks-template.md (✅ updated)
  - .specify/templates/commands/*.md (⚠ pending)
  - README.md (⚠ pending)
  - docs/quickstart.md (⚠ pending)
Follow-up TODOs:
  - Update agent-specific command files to reference new RAG chatbot principles
  - Update README.md to reference RAG governance requirements
  - Create ADR for RAG architecture decisions if not already documented
-->
# Physical AI & Humanoid Robotics Textbook Project Constitution

### Project Vision

To create a high-quality, comprehensive, and engaging AI-native textbook for teaching Physical AI & Humanoid Robotics, leveraging cutting-edge tools and methodologies, and contributing to the Panaversity initiative for AI education.

### Target Audience

This textbook is designed for university students, aspiring AI engineers, robotics enthusiasts, and professionals seeking to understand and implement Physical AI and Humanoid Robotics. Readers are expected to have a foundational understanding of programming (preferably Python) and basic AI/machine learning concepts.

### Definition of "AI-Native Textbook"

An "AI-Native Textbook" in this context refers to a dynamic educational resource that is not only created and maintained with the assistance of AI tools (like Claude Code and Spec-Kit Plus) but also inherently integrates AI as a core component of the learning experience. This includes:

*   AI-Assisted Content Creation: Leveraging AI to generate, refine, and review textual and code content.
*   Integrated RAG Chatbot: Providing an intelligent, conversational AI agent within the book itself that can answer questions, clarify concepts, and guide learning based on the book's specific content.
*   Interactive Learning: Designing the textbook to encourage hands-on application and experimentation, often with simulated or real-world robotic systems, where AI plays a central role.
*   Living Document: The book is expected to be continuously updated and improved, with AI tools facilitating this evolution.

### Core Principles

1.  **Educational Excellence:** The textbook content must be technically accurate, clear, concise, and pedagogical, ensuring effective learning for students.
2.  **AI-Native Development:** Embrace AI-driven development practices, utilizing Claude Code and Spec-Kit Plus to enhance efficiency, quality, and consistency in content creation and feature development.
3.  **Spec-Driven Approach:** Adhere to Spec-Driven Development (SDD) principles, ensuring all features and content are clearly specified, planned, and implemented according to predefined requirements.
4.  **Innovation & Technology:** Actively integrate and leverage specified technologies (Docusaurus, OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, Qdrant Cloud) to build a state-of-the-art interactive learning experience.
5.  **User-Centric Design:** Prioritize the reader's experience, ensuring the textbook is easy to navigate, understand, and interact with, especially through the RAG chatbot.
6.  **Maintainability & Scalability:** Design the book's structure and the RAG chatbot with maintainability and future scalability in mind, allowing for easy updates and expansion.

### Content Style Guide & Tone

The textbook will adopt a clear, accessible, and practical tone. It should be engaging for learners, balancing theoretical concepts with hands-on examples and code snippets. Jargon should be introduced and explained thoroughly. The writing should be formal enough for an academic context but approachable enough to facilitate self-learning.

### Technology & Architecture

1.  **Textbook Platform:** Docusaurus for static site generation and deployment to GitHub Pages.
2.  **AI Development Environment:** Claude Code and Spec-Kit Plus for book creation and feature implementation.
3.  **RAG Chatbot Stack:**
    *   **Agent Framework:** OpenAI Agents/ChatKit SDKs.
    *   **Backend:** FastAPI.
    *   **Package Manager** UV for all python projects
    *   **Vector Database:** Qdrant Cloud (Free Tier).
    *   **Relational Database:** Neon Serverless Postgres.
4.  **Code Quality:** All code contributions must adhere to established best practices, including readability, modularity, and proper error handling.

<!--### Learning Objectives

The textbook will cover the following key learning objectives, enabling students to:

1.  **Physical AI & Embodied Intelligence**
    *   Define Physical AI and embodied intelligence.
    *   Distinguish digital AI from physical-world AI systems.
    *   Understand humanoid robotics and physical-law constraints.
    *   Identify and use core robot sensors (LiDAR, cameras, IMUs, F/T sensors).

2.  **Robotic Control via ROS 2**
    *   Apply ROS 2 architecture: nodes, topics, services, actions.
    *   Build and manage ROS 2 packages in Python.
    *   Use rclpy to bridge AI agents with robot controllers.
    *   Develop robot models using URDF.

3.  **Simulation & Digital Twin Development**
    *   Create physics-accurate simulations in Gazebo.
    *   Use Unity for visualization and interaction scenarios.
    *   Implement URDF/SDF robot descriptions.
    *   Simulate perception sensors (LiDAR, depth, IMU).

4.  **NVIDIA Isaac for Perception & Navigation**
    *   Use NVIDIA Isaac Sim for photorealistic simulation and synthetic data.
    *   Implement Isaac ROS for VSLAM, navigation, and hardware-accelerated perception.
    *   Apply Nav2 for humanoid path planning and locomotion.
    *   Use reinforcement learning and sim-to-real transfer techniques.

5.  **Vision-Language-Action Robotics**
    *   Integrate LLMs for cognitive planning from natural language commands.
    *   Implement speech control using Whisper.
    *   Convert language → action plans executed via ROS 2.
    *   Build multi-modal perception-action loops.

6.  **Humanoid Robotics Engineering**
    *   Apply humanoid kinematics, dynamics, and bipedal locomotion principles.
    *   Develop balance, manipulation, and grasping capabilities.
    *   Design natural human-robot interaction behaviors.

7.  **Conversational Robotics**
    *   Integrate GPT models for conversational and multi-modal interaction.
    *   Implement speech recognition, NLU, and gesture/vision fusion.

8.  **Capstone Requirements**
    *   Build an autonomous humanoid robot simulation.
    *   Process voice commands → LLM planning → ROS 2 action execution.
    *   Navigate, perceive objects, and manipulate them end-to-end.-->

### Ethical Considerations

Given the profound impact of Physical AI and Humanoid Robotics, the textbook will integrate discussions on ethical development, responsible deployment, and societal implications. This includes:

*   **Safety & Reliability:** Emphasizing the design and implementation of robust and safe robotic systems.
*   **Bias & Fairness:** Addressing potential biases in AI models and their impact on physical systems and human interaction.
*   **Privacy & Data Security:** Discussing the ethical handling of data collected by robotic sensors.
*   **Human-Robot Interaction:** Exploring the ethical dimensions of designing natural and respectful interactions with humanoid robots.

### Development Workflow

1.  **Iterative Development:** Adopt an iterative approach, delivering features and content in manageable increments.
2.  **Version Control:** Utilize Git and GitHub for all code and content version control, ensuring a clear history and collaborative environment.
3.  **Prompt History Records (PHRs):** Create detailed PHRs for every significant interaction or development step, ensuring traceability and knowledge capture.
4.  **Architectural Decision Records (ADRs):** Document all architecturally significant decisions with ADRs, outlining options, trade-offs, and rationale.

### Quality Assurance

1.  **Content Review:** Implement a rigorous review process for all textbook content to ensure accuracy, clarity, and adherence to learning objectives.
2.  **Chatbot Testing:** Thoroughly test the RAG chatbot for accuracy, relevance, and robustness in answering questions based on the book's content.
3.  **Deployment Verification:** Ensure that the deployed book and integrated chatbot function correctly on GitHub Pages.

### RAG Chatbot Governance

The integrated RAG chatbot is a critical component of the AI-native learning experience. The following principles govern its development, deployment, and operation:

#### 1. Code Quality & Testing

*   **Unit Testing:** All chatbot backend functions MUST have unit tests with >80% code coverage. Test vector retrieval, prompt construction, and response generation independently.
*   **Integration Testing:** End-to-end tests MUST verify the complete RAG pipeline: query → retrieval → generation → response with citations.
*   **PEP 8 Compliance:** All Python code MUST adhere to PEP 8 style guidelines. Use automated linters (pylint, flake8, black) in CI/CD pipelines.
*   **Documentation:** Every function and API endpoint MUST include docstrings explaining purpose, parameters, return values, and exceptions. Use type hints (typing module) for all function signatures.
*   **Error Handling:** Implement comprehensive error handling for vector database failures, LLM API errors, and malformed queries. Log errors with contextual information.

**Rationale:** High code quality ensures maintainability, reduces bugs, and enables confident iterations. Testing validates the RAG pipeline's correctness and reliability.

#### 2. User Experience Requirements

*   **Responsive Design:** The chat widget MUST be fully responsive, functioning seamlessly on desktop (≥1024px), tablet (768-1023px), and mobile (≤767px) viewports.
*   **Accessibility (WCAG 2.1 Level AA):**
    *   Keyboard navigation MUST work for all chat interactions (focus visible, tab order logical).
    *   Screen reader compatibility MUST be verified (ARIA labels, semantic HTML).
    *   Color contrast ratios MUST meet WCAG AA standards (≥4.5:1 for normal text).
*   **Citation Display:** Every chatbot response MUST clearly display source citations with:
    *   Page/section titles linked to the original content.
    *   Visual distinction (e.g., footnote-style references, highlighted excerpts).
    *   No hallucinated references; all citations MUST correspond to actual book content.
*   **Response Time:** 95th percentile response latency MUST be ≤2 seconds from query submission to first token displayed (including retrieval + generation).
*   **Loading States:** Display clear loading indicators during query processing. Provide graceful degradation messages if services are unavailable.

**Rationale:** User experience directly impacts learning effectiveness. Accessibility ensures inclusivity. Fast response times and clear citations build trust and usability.

#### 3. Security & Privacy

*   **No PII Storage:** The chatbot MUST NOT persist any personally identifiable information (names, emails, IP addresses beyond session management).
*   **Prompt Injection Sanitization:**
    *   User queries MUST be sanitized to prevent prompt injection attacks (e.g., "Ignore previous instructions...").
    *   Implement input validation: strip system-level commands, limit query length (≤1000 chars), detect and block malicious patterns.
*   **Restricted Admin Access:**
    *   Admin endpoints (e.g., vector database reindexing, configuration changes) MUST require authentication (API keys, OAuth).
    *   Use environment variables for secrets; NEVER hardcode API keys or database credentials.
*   **Rate Limiting:** Implement per-IP rate limits (e.g., 60 queries/hour) to prevent abuse and DoS attempts.
*   **Data Encryption:** Use HTTPS for all client-server communication. Encrypt sensitive configuration at rest (e.g., database connection strings).

**Rationale:** Security protects users and the system. Privacy compliance respects learners' data. Sanitization prevents exploitation of LLM vulnerabilities.

#### 4. Performance Expectations

*   **Asynchronous Design:** All I/O operations (database queries, LLM API calls, vector search) MUST use async/await patterns (FastAPI with asyncio).
*   **No Blocking Calls:** Synchronous blocking calls in request handlers are PROHIBITED. Use non-blocking HTTP clients (httpx) and async database drivers.
*   **Latency Monitoring:**
    *   Instrument each pipeline stage (retrieval time, generation time, total response time) with metrics (Prometheus, CloudWatch, or equivalent).
    *   Set up alerts for P95 latency exceeding 2.5s or error rates >1%.
*   **Resource Limits:**
    *   Limit concurrent LLM API calls (e.g., max 10 concurrent requests) to avoid quota exhaustion.
    *   Implement connection pooling for Postgres and Qdrant to optimize database access.
*   **Caching Strategy:** Cache frequent queries (TTL 1 hour) to reduce redundant vector searches and LLM calls.

**Rationale:** Asynchronous design ensures scalability and responsiveness. Monitoring enables proactive issue detection. Resource limits prevent service degradation under load.

#### 5. RAG & Citation Discipline

*   **Grounded Answers:** All chatbot responses MUST be grounded in the textbook content. If the retrieved context does not contain sufficient information, the chatbot MUST respond: "I don't have enough information in the book to answer that question. Please refer to [relevant chapter] or rephrase your query."
*   **Source Attribution:** Every factual claim MUST cite the specific page/section where the information originates. Use retrieval metadata (document IDs, section titles) to construct citations.
*   **No Hallucination:** The chatbot MUST NOT generate information outside the textbook content. Implement confidence thresholds: if retrieval similarity score <0.7, trigger the "insufficient information" response.
*   **Context Window Management:** Limit retrieved context to top 5 relevant chunks (≤2000 tokens total) to fit within LLM context windows and reduce noise.
*   **Citation Validation:** Periodically audit chatbot responses to verify citation accuracy. Flag and correct any hallucinated references.

**Rationale:** Grounded answers maintain educational integrity. Clear citations enable learners to verify and deepen understanding. Preventing hallucinations builds trust.

#### 6. Maintainability Standards

*   **Framework Discipline:** Use FastAPI for backend services. Avoid unnecessary abstractions; keep routing logic simple and declarative.
*   **ChatKit SDK Usage:** Follow OpenAI ChatKit SDK best practices. Do not fork or heavily customize; rely on official APIs to simplify upgrades.
*   **Architecture Documentation:**
    *   Maintain a `docs/rag-architecture.md` file documenting:
        *   System architecture diagram (frontend ↔ FastAPI ↔ Qdrant/Postgres ↔ OpenAI API).
        *   Data flow for queries and responses.
        *   Deployment topology (local dev, staging, production).
    *   Update documentation with every significant architectural change.
*   **Quick-Start Guide:** Provide a `docs/rag-quickstart.md` with:
    *   Local development setup (dependencies, environment variables, database initialization).
    *   Running unit and integration tests.
    *   Deploying to production (CI/CD pipeline overview).
*   **Dependency Management:** Pin exact versions in `requirements.txt` or `pyproject.toml`. Review and update dependencies quarterly for security patches.
*   **Code Reviews:** All RAG chatbot code changes MUST undergo peer review. Check for adherence to these principles before merging.

**Rationale:** Maintainability ensures the chatbot evolves with the textbook. Documentation reduces onboarding friction. Disciplined framework usage prevents technical debt.

### Success Metrics

The success of this project will be measured by:

*   **Educational Impact:** Demonstrated student learning outcomes as defined by the learning objectives.
*   **Content Quality:** High ratings for clarity, accuracy, and engagement from pilot users or peer reviews.
*   **RAG Chatbot Performance:**
    *   **Accuracy:** >90% of chatbot responses accurately grounded in textbook content (measured via manual review of sample queries).
    *   **Citation Precision:** 100% of citations correspond to actual book content (zero hallucinated references).
    *   **Response Latency:** P95 response time ≤2 seconds; P99 ≤3 seconds.
    *   **User Satisfaction:** >4.0/5.0 rating for chatbot helpfulness (via in-app feedback).
    *   **Uptime:** 99.5% availability (excluding planned maintenance).
*   **Technical Robustness:** Stable deployment of the Docusaurus book and the integrated RAG chatbot.
*   **Security & Privacy Compliance:** Zero security incidents related to PII leakage or prompt injection exploits.
*   **Code Quality Metrics:**
    *   Test coverage >80% for RAG backend code.
    *   All linter checks passing (PEP 8 compliance).
    *   Zero critical or high-severity vulnerabilities in dependencies (Snyk/Dependabot scans).
*   **Community Engagement (Panaversity):** Positive feedback and adoption within the Panaversity ecosystem.

## Governance

This Constitution supersedes all other project practices and documentation. Amendments to this Constitution require:

1.  Documentation of proposed changes and their rationale.
2.  Approval by key stakeholders.
3.  A comprehensive migration plan for any dependent artifacts.

All pull requests and code reviews must verify compliance with the principles outlined herein. Any introduced complexity must be thoroughly justified. The `.specify/memory/constitution.md` file serves as the definitive source for these guidelines.

**Version**: 1.1.0 | **Ratified**: 2025-11-28 | **Last Amended**: 2025-12-01
