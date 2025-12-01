# Feature Specification: RAG Chatbot Integration

**Feature Branch**: `011-rag-chatbot-integration`
**Created**: 2025-12-01
**Status**: Draft
**Input**: User description: "Build a production-ready RAG (Retrieval-Augmented Generation) chatbot system that integrates with our Docusaurus documentation website to answer user questions based on the book content."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions About Book Content (Priority: P1)

As a reader of the Physical AI & Humanoid Robotics textbook, I want to ask questions about concepts in the book and receive AI-generated answers with source citations, so that I can quickly clarify confusing topics without manually searching through chapters.

**Why this priority**: This is the core value proposition of the RAG chatbot. Without this functionality, the feature provides no user value. It's the minimum viable product that demonstrates the chatbot's ability to answer questions based on book content.

**Independent Test**: Can be fully tested by opening any documentation page, clicking the chat button, typing "What is Physical AI?", and verifying that the chatbot returns a relevant answer with at least 3 source citations from the book content.

**Acceptance Scenarios**:

1. **Given** I am on any documentation page, **When** I click the floating chat button, **Then** the chat window opens showing a welcome message
2. **Given** the chat window is open, **When** I type "What is ROS2?" and press Enter, **Then** I receive an answer within 3 seconds with relevant citations
3. **Given** I receive an answer, **When** I review the sources, **Then** each citation shows the page title, relevance score, and clickable link to the source page
4. **Given** I ask a question outside the book's scope (e.g., "What is the weather?"), **When** the chatbot responds, **Then** it clearly states it can only answer questions about book content

---

### User Story 2 - Context-Aware Follow-up Questions (Priority: P2)

As a reader learning complex robotics concepts, I want to ask follow-up questions that reference my previous conversation, so that I can have a natural dialogue without repeating context.

**Why this priority**: This enhances the learning experience by enabling natural conversation flow. While not essential for basic functionality, it significantly improves usability and makes the chatbot feel more intelligent.

**Independent Test**: Can be tested independently by starting a new conversation, asking "What is ROS2?", receiving an answer, then asking "What are its main components?" and verifying the chatbot understands "its" refers to ROS2 from the previous message.

**Acceptance Scenarios**:

1. **Given** I have asked "What is Physical AI?" and received an answer, **When** I ask "What are its key components?", **Then** the chatbot understands "its" refers to Physical AI
2. **Given** I have an active conversation with 5 messages, **When** I refresh the page, **Then** my conversation history persists and I can continue the dialogue
3. **Given** I have multiple conversation sessions, **When** I return to the documentation, **Then** the chatbot remembers my most recent session

---

### User Story 3 - Ask Questions About Selected Text (Priority: P3)

As a reader who encounters confusing passages, I want to select specific text on the page and ask the chatbot to explain it in simpler terms, so that I can get targeted help on exactly what I don't understand.

**Why this priority**: This is a power-user feature that adds significant convenience but isn't required for basic functionality. It represents an advanced interaction pattern that enhances precision.

**Independent Test**: Can be tested by selecting the text "Embodied intelligence is built upon a continuous cycle" on any page, seeing a yellow context banner appear, asking "Explain this in simple terms", and verifying the answer specifically addresses the selected text.

**Acceptance Scenarios**:

1. **Given** I am reading a documentation page, **When** I select text between 1-1000 characters, **Then** a yellow banner appears saying "📝 Using selected text as context"
2. **Given** text is selected and the context banner is visible, **When** I type a question and send it, **Then** the chatbot's answer specifically references and explains the selected text
3. **Given** the context banner is showing, **When** I click the X button, **Then** the selected text context is cleared
4. **Given** I have selected text, **When** I select different text, **Then** the context updates to the new selection

---

### User Story 4 - Mobile-Friendly Chat Experience (Priority: P2)

As a mobile user reading the documentation on my phone, I want a responsive chat interface that works well on small screens, so that I can get help even when away from my computer.

**Why this priority**: Mobile users represent a significant portion of documentation readers. While desktop is primary, mobile support is essential for modern web applications and affects accessibility.

**Independent Test**: Can be tested by opening the documentation on a mobile device (viewport ≤767px), clicking the chat button, and verifying the chat window expands to full screen with properly sized touch targets.

**Acceptance Scenarios**:

1. **Given** I am on a mobile device, **When** I click the chat button, **Then** the chat window expands to full screen
2. **Given** the chat is open on mobile, **When** I type and send a message, **Then** the virtual keyboard doesn't obscure the input field
3. **Given** I am viewing sources on mobile, **When** I click a source citation, **Then** it opens the source page in a way that allows easy navigation back
4. **Given** I am in dark mode on mobile, **When** I open the chat, **Then** the chat interface uses appropriate dark mode colors

---

### User Story 5 - Clear Loading and Error States (Priority: P3)

As a user waiting for a chatbot response, I want clear visual feedback showing the system is working, so that I know my question was received and the system hasn't frozen.

**Why this priority**: This improves user experience and reduces confusion, but the chatbot can function without sophisticated loading states. It's a polish feature that enhances perception of reliability.

**Independent Test**: Can be tested by asking a question and immediately observing an animated loading indicator (three dots), then simulating a backend failure and verifying a helpful error message appears.

**Acceptance Scenarios**:

1. **Given** I have sent a message, **When** waiting for a response, **Then** I see an animated loading indicator (three dots)
2. **Given** the backend is unavailable, **When** I send a message, **Then** I receive a clear error message explaining the issue and suggesting I try again
3. **Given** my query takes longer than expected, **When** waiting, **Then** the loading state remains visible (no timeout confusion)
4. **Given** an error occurs, **When** I retry my question, **Then** the chatbot attempts the request again

---

### Edge Cases

- What happens when a user selects more than 1000 characters of text?
  - **Expected**: The system ignores selections over 1000 characters and does not show the context banner
- How does the system handle queries with special characters or code snippets?
  - **Expected**: The system sanitizes input to prevent prompt injection while preserving legitimate special characters needed for technical questions
- What happens when no relevant content is found in the vector database?
  - **Expected**: The chatbot responds with "I don't have information about that in the documentation. I can only answer questions about Physical AI, robotics, ROS2, and related topics covered in this book."
- How does the system behave when the OpenAI API rate limit is exceeded?
  - **Expected**: The system returns a user-friendly error message: "The chatbot is experiencing high demand. Please try again in a moment."
- What happens when a user's session has been idle for more than 7 days?
  - **Expected**: The session expires and the conversation history is cleared, starting fresh on next interaction
- How does the system handle concurrent requests from the same user?
  - **Expected**: The system queues requests sequentially, showing loading states for each, preventing race conditions
- What happens if the user closes the chat window while a response is loading?
  - **Expected**: The request completes in the background, and the response is available when the chat is reopened
- How does the system handle markdown formatting in chatbot responses?
  - **Expected**: The chatbot renders markdown properly (bold, italic, lists, code blocks) for readable formatting

## Requirements *(mandatory)*

### Functional Requirements

#### Core RAG Functionality

- **FR-001**: System MUST generate embeddings for user queries using a 1536-dimension embedding model
- **FR-002**: System MUST search the vector database and retrieve the top 5 most semantically similar document chunks for each query
- **FR-003**: System MUST provide relevance scores (0-1 scale) for each retrieved document chunk
- **FR-004**: System MUST use retrieved context to generate AI responses that are grounded in the book content
- **FR-005**: System MUST display source citations with every answer, including page/section title, file path, and relevance percentage
- **FR-006**: System MUST refuse to answer questions outside the book's scope with a clear explanation of its limitations

#### Document Indexing

- **FR-007**: System MUST index all markdown/MDX files from the `docs/` directory on initialization
- **FR-008**: System MUST extract frontmatter metadata (title, sidebar_position) from each document
- **FR-009**: System MUST chunk documents into overlapping segments of approximately 1000 words per chunk with 200-word overlap
- **FR-010**: System MUST store document chunks with metadata (title, file_path, chunk_index, total_chunks) in the vector database
- **FR-011**: System MUST clean markdown content by removing code blocks and converting to plain text before chunking

#### Conversation Management

- **FR-012**: System MUST create a unique session ID for each new conversation
- **FR-013**: System MUST persist conversation history in a relational database with message content, role (user/assistant), timestamp, and optional selected_text
- **FR-014**: System MUST maintain conversation context across multiple messages within a session
- **FR-015**: System MUST retrieve and display full conversation history when requested via API endpoint
- **FR-016**: System MUST expire sessions after 7 days of inactivity

#### User Interface

- **FR-017**: System MUST display a floating chat button (💬 icon) in the bottom-right corner on all documentation pages
- **FR-018**: System MUST open a chat window (400px × 600px on desktop) when the chat button is clicked
- **FR-019**: System MUST expand chat to full screen on mobile devices (viewport ≤767px)
- **FR-020**: System MUST display user messages with purple gradient styling and assistant messages with neutral white/gray styling
- **FR-021**: System MUST show an animated loading indicator (three dots) while waiting for responses
- **FR-022**: System MUST auto-scroll to the newest message when new content arrives
- **FR-023**: System MUST persist session in browser localStorage so conversation survives page reloads
- **FR-024**: System MUST support sending messages via Enter key or button click
- **FR-025**: System MUST provide a "Clear conversation" button to start a new session

#### Text Selection Feature

- **FR-026**: System MUST detect when user selects text on the documentation page
- **FR-027**: System MUST display a yellow banner "📝 Using selected text as context" when text between 1-1000 characters is selected
- **FR-028**: System MUST include selected text in the API request as additional context
- **FR-029**: System MUST clear selected text context after message is sent or user clicks the X button
- **FR-030**: System MUST ignore text selections under 1 character or over 1000 characters

#### API Endpoints

- **FR-031**: System MUST provide a `GET /api/health` endpoint returning status of all services (Qdrant, Postgres, OpenAI connectivity)
- **FR-032**: System MUST provide a `POST /api/chat` endpoint accepting {message, session_id?, selected_text?} and returning {session_id, message, sources[], timestamp}
- **FR-033**: System MUST provide a `GET /api/sessions/{session_id}/history` endpoint returning full conversation history in chronological order

#### Accessibility & Responsiveness

- **FR-034**: System MUST support keyboard navigation (Tab, Enter, Esc) for all chat interactions
- **FR-035**: System MUST provide ARIA labels for screen reader compatibility
- **FR-036**: System MUST maintain color contrast ratios of at least 4.5:1 (WCAG AA standard)
- **FR-037**: System MUST support both light and dark mode via `[data-theme='dark']` CSS selectors
- **FR-038**: System MUST render properly on desktop (≥1024px), tablet (768-1023px), and mobile (≤767px) viewports

#### Error Handling & Validation

- **FR-039**: System MUST validate all user inputs using schema validation (Pydantic models on backend, TypeScript interfaces on frontend)
- **FR-040**: System MUST sanitize user queries to prevent prompt injection attacks (strip system-level commands, detect malicious patterns)
- **FR-041**: System MUST display user-friendly error messages when backend services are unavailable
- **FR-042**: System MUST handle transient API failures with automatic retry logic (up to 3 retries with exponential backoff)
- **FR-043**: System MUST limit query length to 1000 characters to prevent abuse

#### Security & Privacy

- **FR-044**: System MUST NOT persist personally identifiable information (names, emails, IP addresses beyond session management)
- **FR-045**: System MUST configure CORS to accept requests only from specified allowed origins
- **FR-046**: System MUST store all API keys and database credentials in environment variables
- **FR-047**: System MUST use HTTPS for all client-server communication in production
- **FR-048**: System MUST log errors with contextual information but MUST NOT log sensitive data (API keys, user content)

### Key Entities

- **ChatSession**: Represents a conversation session between a user and the chatbot
  - Attributes: unique session ID (UUID), creation timestamp, last activity timestamp
  - Relationships: has many ChatMessages
  - Lifecycle: created on first message, expires after 7 days of inactivity

- **ChatMessage**: Represents a single message in a conversation
  - Attributes: unique message ID (UUID), session ID (foreign key), role (user/assistant), message content, optional selected_text, optional context_used, timestamp
  - Relationships: belongs to one ChatSession
  - Lifecycle: created when user sends message or assistant responds, persisted indefinitely (subject to session expiration)

- **DocumentChunk**: Represents a searchable chunk of documentation content in the vector database
  - Attributes: unique chunk ID, document title, file path, chunk text content, chunk index, total chunks in document, embedding vector (1536 dimensions), metadata (frontmatter)
  - Relationships: belongs to one source document, retrieved by queries
  - Lifecycle: created during initial indexing, updated when documentation changes

- **Source**: Represents a citation returned with chatbot answers
  - Attributes: document title, file path, relevance score (0-1), chunk text excerpt
  - Relationships: derived from DocumentChunk during retrieval
  - Lifecycle: ephemeral, created per query response

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can receive answers to book-related questions within 3 seconds for 95% of queries
- **SC-002**: System accurately answers at least 90% of questions that are covered in the book content (measured via manual review of 100 sample queries)
- **SC-003**: Every chatbot response includes at least 1 relevant source citation, with 100% of citations corresponding to actual book content (zero hallucinated references)
- **SC-004**: Average relevance score for the top-ranked source is above 0.70 (70% similarity)
- **SC-005**: System successfully handles 10 concurrent users without response time degradation
- **SC-006**: Mobile users (viewport ≤767px) can successfully complete the full question-answer flow with no usability issues
- **SC-007**: Chat interface achieves 60fps smooth animations during open/close transitions (verified via browser DevTools)
- **SC-008**: System maintains 95%+ uptime over a 30-day period (excluding planned maintenance)
- **SC-009**: Zero security incidents related to PII leakage or prompt injection exploits in production
- **SC-010**: Users report >4.0/5.0 average satisfaction rating for chatbot helpfulness (measured via optional in-app feedback)
- **SC-011**: Task completion rate for "find answer to a specific question" improves by 40% compared to manual search
- **SC-012**: System error rate remains below 5% of all requests
- **SC-013**: Conversation history successfully persists across page reloads for 100% of sessions
- **SC-014**: Text selection feature works correctly for 100% of valid text selections (1-1000 characters)
- **SC-015**: All 5 comprehensive test cases pass (health check, basic chat, context-aware chat, text selection, session history)

### Quality Standards

- **SC-016**: Backend code achieves >80% test coverage with all unit and integration tests passing
- **SC-017**: All Python code passes PEP 8 linting with zero violations
- **SC-018**: All TypeScript code is fully type-safe with zero type errors
- **SC-019**: Documentation is complete with setup instructions, API reference, and troubleshooting guide
- **SC-020**: Zero critical or high-severity vulnerabilities in dependencies (verified via Snyk or Dependabot scans)

### Cost & Performance

- **SC-021**: Monthly operating cost remains under $15 for moderate usage (up to 1000 queries/month)
- **SC-022**: Backend setup time is under 2 hours (excluding external service signups)
- **SC-023**: Frontend integration time is under 1 hour
- **SC-024**: System can index 1000+ documentation files without performance degradation
- **SC-025**: Vector database can handle 10,000+ document chunks with search latency <50ms

## Assumptions

The following assumptions are made based on industry standards and common practices:

1. **Deployment Environment**: The system will be deployed with the backend on a cloud platform (Railway/Render) and frontend integrated into the existing Docusaurus GitHub Pages deployment
2. **User Load**: Moderate usage is defined as approximately 1000 queries per month, with peak concurrent usage of 10-20 users
3. **Documentation Structure**: The Docusaurus `docs/` directory follows standard conventions with markdown/MDX files containing frontmatter metadata
4. **Browser Support**: Modern browsers are assumed (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
5. **Network Conditions**: Users have stable internet connections with reasonable latency (<500ms to cloud services)
6. **External Services**: OpenAI API, Qdrant Cloud, and Neon Postgres free tiers will be sufficient for initial deployment and moderate usage
7. **Content Updates**: Documentation content changes are infrequent enough that manual re-indexing is acceptable (no automatic webhook-based indexing required initially)
8. **Session Management**: Session expiration after 7 days is acceptable for educational content (users don't need long-term conversation persistence)
9. **Localization**: Initial version supports English only; no multi-language requirements
10. **Authentication**: No user authentication is required; chatbot is publicly accessible to all documentation readers

## Constraints

### Technology Constraints

- **TC-001**: MUST use OpenAI for embeddings (text-embedding-3-small) and chat completions (GPT-4o-mini)
- **TC-002**: MUST use Qdrant Cloud free tier for vector database (no local Qdrant instance)
- **TC-003**: MUST use Neon Serverless Postgres free tier for relational database
- **TC-004**: MUST integrate with existing Docusaurus v3+ site without breaking current functionality
- **TC-005**: MUST work in both WSL/Linux and Windows development environments
- **TC-006**: MUST use React with TypeScript for frontend components
- **TC-007**: MUST use FastAPI for backend REST API
- **TC-008**: MUST use Docusaurus theme swizzling for global integration (no configuration changes to docusaurus.config.js)

### Budget Constraints

- **BC-001**: Total monthly operating cost MUST remain under $15
- **BC-002**: MUST use free tiers for Qdrant Cloud (1GB storage) and Neon Postgres (0.5GB storage)
- **BC-003**: OpenAI API costs MUST stay under $10/month through token optimization (limit context length, efficient prompts)

### Time Constraints

- **TIC-001**: Backend implementation MUST be completable within 2 hours (excluding external service signups)
- **TIC-002**: Frontend implementation MUST be completable within 1 hour
- **TIC-003**: Testing MUST be completable within 30 minutes
- **TIC-004**: Documentation MUST be completable within 1 hour

### Integration Constraints

- **IC-001**: MUST NOT break existing Docusaurus functionality
- **IC-002**: MUST NOT require changes to Docusaurus configuration files
- **IC-003**: MUST work with existing documentation content structure (no modifications to existing .md/.mdx files)
- **IC-004**: MUST render after Docusaurus page content loads (not block initial page render)

### Scope Constraints (Explicitly Out of Scope)

- **SC-OUT-001**: Voice input/output
- **SC-OUT-002**: Multi-language support
- **SC-OUT-003**: User authentication and accounts
- **SC-OUT-004**: Conversation sharing/export functionality
- **SC-OUT-005**: Admin dashboard or analytics UI
- **SC-OUT-006**: Rate limiting at application level (rely on API provider rate limits)
- **SC-OUT-007**: Caching layer (beyond simple query caching)
- **SC-OUT-008**: Custom LLM fine-tuning
- **SC-OUT-009**: Feedback collection UI
- **SC-OUT-010**: Search history or suggested questions
- **SC-OUT-011**: Multi-modal input (images, files, audio)

## Dependencies

### External Services

- **OpenAI API**: Required for embeddings and chat completions
  - Signup required: https://platform.openai.com/signup
  - API key required: OPENAI_API_KEY environment variable
  - Free tier: $5 free credit (sufficient for initial testing)

- **Qdrant Cloud**: Required for vector database
  - Signup required: https://cloud.qdrant.io/
  - API key required: QDRANT_URL and QDRANT_API_KEY environment variables
  - Free tier: 1GB storage (sufficient for 10,000+ document chunks)

- **Neon Serverless Postgres**: Required for conversation storage
  - Signup required: https://neon.tech/
  - Connection string required: DATABASE_URL environment variable
  - Free tier: 0.5GB storage (sufficient for thousands of conversations)

### Technical Dependencies

- **Backend**: Python 3.9+, FastAPI, SQLAlchemy, Pydantic, python-dotenv, markdown, beautifulsoup4, tiktoken, openai, qdrant-client, psycopg2-binary,UV
- **Package Manager** : Use UV package manager for python
- **Frontend**: React 18+, TypeScript 4.9+, Docusaurus 3+
- **Development Tools**: Node.js 18+, npm/yarn, Python package manager, Git

### Infrastructure Dependencies

- **Deployment Platform**: Cloud hosting for FastAPI backend (Railway, Render, or similar)
- **DNS/Hosting**: GitHub Pages for Docusaurus frontend (already in place)
- **CORS Configuration**: Backend must be configured to accept requests from GitHub Pages domain

## Reference Metrics (from Working Implementation)

The following metrics are provided from a verified working implementation to guide expectations:

- **Total Files Created**: 15 (12 backend Python files, 3 frontend TypeScript/CSS files)
- **Lines of Code**: ~2500 total (Python: ~1500, TypeScript/CSS: ~1000)
- **Test Coverage**: 100% (5/5 comprehensive test cases passing)
- **Average Response Time**: 1.5-2.5 seconds (well under 3-second requirement)
- **Average Relevance Score**: 55-75% for top results (indicates good semantic matching)
- **Actual Cost**: $5-10/month for 1000 queries (within budget)
- **Setup Time**: 10 minutes (excluding service signups, once dependencies are installed)
- **Deployment Time**: 15 minutes (from code complete to production)

These metrics demonstrate that the requirements are achievable and provide realistic targets for implementation planning.
