# Implementation Tasks: RAG Chatbot Integration

**Feature**: 011-rag-chatbot-integration
**Branch**: `011-rag-chatbot-integration`
**Generated**: 2025-12-01
**Total Tasks**: 52

---

## Overview

This document contains all implementation tasks for the RAG chatbot integration feature, organized by user story for independent implementation and testing. Each task follows the strict checklist format with task IDs, parallelization markers, story labels, and explicit file paths.

**Task Format**: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- **[P]**: Task can be parallelized (different files, no dependencies)
- **[Story]**: User story label (US1-US5) for story-specific tasks

---

## Implementation Strategy

**MVP Scope**: User Story 1 (P1) - Core RAG chatbot functionality
- After completing US1, you have a working chatbot that answers questions with citations
- This represents the minimum viable product for user value

**Incremental Delivery Order**:
1. Setup & Foundational (blocking prerequisites)
2. **US1** (P1) - Core RAG chatbot ← **MVP**
3. **US2** (P2) - Context-aware follow-ups (already built into US1)
4. **US4** (P2) - Mobile responsive design
5. **US3** (P3) - Text selection feature
6. **US5** (P3) - Loading/error states polish
7. Polish & Cross-cutting concerns

---

## Dependencies & Execution Order

### Story Dependency Graph

```
Setup Phase (Phase 1)
        ↓
Foundational Phase (Phase 2)
        ↓
    ┌───┴───┐
    ↓       ↓
   US1*   (Can start others after US1 backend complete)
    ↓
    ├──→ US2 (actually built into US1)
    ├──→ US4 (independent frontend work)
    ├──→ US3 (depends on US1 frontend)
    └──→ US5 (depends on US1 frontend)
        ↓
    Polish Phase

* = Blocking story (US1 must complete before other stories)
```

### Parallel Opportunities

**Phase 1 (Setup)**: Tasks T001-T009 can run in sequence (project setup)

**Phase 2 (Foundational)**: Tasks T010-T015 are partially parallelizable
- T010, T011 can run in parallel (different databases)
- T012-T015 can run in parallel (different services)

**Phase 3 (US1)**: Tasks T016-T033 have parallel opportunities
- Backend models (T016-T017) can run in parallel
- Backend services (T018-T023) can run in parallel after models
- API endpoints (T024-T026) can run in parallel after services
- Frontend components (T027-T032) can run in parallel

**Phase 4-7**: User stories US2-US5 are largely independent and can be parallelized

---

## Phase 1: Setup

**Goal**: Initialize project structure, install dependencies, configure external services

**Duration Estimate**: 2-3 hours (including service signups)

### Tasks

- [X] T001 Create backend directory structure at `backend/src/{models,services,api,utils}`
- [X] T002 Create backend test directory structure at `backend/tests/{unit,integration}`
- [X] T003 Create scripts directory at `backend/scripts`
- [X] T004 Create pyproject.toml with UV package manager configuration at `backend/pyproject.toml`
- [ ] T005 Install Python dependencies using UV package manager
- [X] T006 Create .env.example file at `backend/.env.example` with all required environment variables
- [ ] T007 Configure external services (OpenAI API key, Qdrant Cloud cluster, Neon Postgres database)
- [ ] T008 Create .env file at `backend/.env` with actual credentials (not committed to Git)
- [X] T009 Add backend/.env to .gitignore to prevent credential leaks

**Completion Criteria**:
- Backend directory structure matches plan.md specifications
- All Python dependencies installed successfully
- External services (OpenAI, Qdrant, Neon) provisioned and accessible
- .env file configured with valid credentials

---

## Phase 2: Foundational

**Goal**: Set up databases, core configuration, and shared utilities (blocking prerequisites for all user stories)

**Duration Estimate**: 1-2 hours

### Tasks

- [ ] T010 Apply Postgres schema from `specs/011-rag-chatbot-integration/contracts/database-schema.sql` to Neon database
- [ ] T011 Create Qdrant collection using configuration from `specs/011-rag-chatbot-integration/contracts/qdrant-schema.json`
- [X] T012 [P] Implement configuration management in `backend/src/config.py` (load environment variables with Pydantic Settings)
- [X] T013 [P] Implement markdown parser in `backend/src/utils/markdown.py` (extract text, remove code blocks)
- [X] T014 [P] Implement input sanitization in `backend/src/utils/sanitization.py` (prompt injection prevention, validation)
- [X] T015 [P] Create indexing script at `backend/scripts/index_docs.py` (chunk documents, generate embeddings, upload to Qdrant)

**Completion Criteria**:
- Postgres tables (chat_sessions, chat_messages) created with indexes and triggers
- Qdrant collection (documentation_chunks) created with vector configuration
- Configuration module loads all environment variables correctly
- Utility functions (markdown parsing, sanitization) implemented and tested
- Indexing script can process documentation files and upload to Qdrant

**Test**:
- Run indexing script: `python backend/scripts/index_docs.py --docs-dir docs`
- Verify Qdrant contains document chunks: Check collection point count > 0

---

## Phase 3: User Story 1 - Core RAG Chatbot (P1) ⭐ MVP

**Story**: As a reader of the Physical AI & Humanoid Robotics textbook, I want to ask questions about concepts in the book and receive AI-generated answers with source citations, so that I can quickly clarify confusing topics without manually searching through chapters.

**Goal**: Implement complete RAG pipeline (backend + frontend) for question answering with citations

**Duration Estimate**: 4-6 hours

**Independent Test**: Open any documentation page, click chat button, type "What is Physical AI?", verify response with 3+ source citations appears within 3 seconds

### Backend Models

- [X] T016 [P] [US1] Create Pydantic models for Chat domain in `backend/src/models/chat.py` (ChatRequest, ChatResponse, ChatMessage, ChatSession)
- [X] T017 [P] [US1] Create Pydantic models for Document domain in `backend/src/models/document.py` (DocumentChunk, Source)

### Backend Services

- [X] T018 [P] [US1] Implement OpenAI embeddings service in `backend/src/services/embedding.py` (generate query embeddings using text-embedding-3-small)
- [X] T019 [P] [US1] Implement Qdrant vector store service in `backend/src/services/vector_store.py` (semantic search, retrieve top 5 chunks, filter by threshold 0.7)
- [X] T020 [P] [US1] Implement OpenAI LLM service in `backend/src/services/llm.py` (generate grounded responses using GPT-4o-mini, system prompt with context)
- [X] T021 [P] [US1] Implement conversation persistence service in `backend/src/services/conversation.py` (create/retrieve sessions, save messages, SQLAlchemy async with asyncpg)
- [X] T022 [US1] Implement RAG orchestration service in `backend/src/services/rag_service.py` (coordinate embedding → search → LLM pipeline)
- [X] T023 [US1] Add error handling and logging to all services (OpenAI errors, Qdrant failures, Postgres timeouts)

### Backend API Endpoints

- [X] T024 [P] [US1] Implement health check endpoint in `backend/src/api/health.py` (GET /api/health, check Qdrant/Postgres/OpenAI connectivity)
- [X] T025 [US1] Implement chat endpoint in `backend/src/api/chat.py` (POST /api/chat, RAG pipeline, return response with sources)
- [X] T026 [P] [US1] Implement session history endpoint in `backend/src/api/sessions.py` (GET /api/sessions/{id}/history, retrieve chronological messages)

### Backend Application

- [X] T027 [US1] Create FastAPI application in `backend/src/main.py` (app initialization, CORS middleware, route registration, lifespan events)
- [X] T028 [US1] Configure CORS to allow frontend origins (localhost:3000 and GitHub Pages domain)
- [X] T029 [US1] Add request/response logging middleware to FastAPI app

### Frontend Setup

- [X] T030 [US1] Swizzle Docusaurus Root component: `npm run swizzle @docusaurus/theme-classic Root -- --eject` creates `src/theme/Root.tsx`
- [X] T031 [US1] Create ChatWidget directory structure at `src/theme/components/ChatWidget/`

### Frontend Components

- [X] T032 [P] [US1] Implement ChatButton component in `src/theme/components/ChatWidget/ChatButton.tsx` (floating button, bottom-right, onClick toggle)
- [X] T033 [P] [US1] Implement ChatWindow component in `src/theme/components/ChatWidget/ChatWindow.tsx` (400px × 600px container, open/close animation)
- [X] T034 [P] [US1] Implement MessageList component in `src/theme/components/ChatWidget/MessageList.tsx` (render user/assistant messages, auto-scroll)
- [X] T035 [P] [US1] Implement InputArea component in `src/theme/components/ChatWidget/InputArea.tsx` (text input, send button, Enter key handler)
- [X] T036 [P] [US1] Implement SourceCitation component in `src/theme/components/ChatWidget/SourceCitation.tsx` (display sources with title, score, link)
- [X] T037 [US1] Create ChatWidget main component in `src/theme/components/ChatWidget/index.tsx` (orchestrate all child components, manage state)
- [X] T038 [US1] Implement API client in `src/theme/components/ChatWidget/api/chatApi.ts` (fetch wrapper for /api/chat, error handling)

### Frontend Integration

- [X] T039 [US1] Update Root.tsx to render ChatWidget globally with lazy loading
- [X] T040 [US1] Implement session persistence in localStorage (save/restore session_id and messages across page reloads)
- [X] T041 [US1] Style ChatWidget components in `src/theme/components/ChatWidget/styles.module.css` (purple gradient for user messages, neutral for assistant)

### Testing & Verification

- [ ] T042 [US1] Test backend health endpoint: `curl http://localhost:8000/api/health` returns all services "up"
- [ ] T043 [US1] Test chat endpoint with sample query: Verify response with sources
- [ ] T044 [US1] Test frontend: Open documentation page, click chat button, send "What is Physical AI?", verify response with 3+ citations within 3 seconds
- [ ] T045 [US1] Test out-of-scope query: Ask "What is the weather?", verify chatbot states it can only answer book questions

**Completion Criteria**:
- ✅ Backend: All services implemented with error handling
- ✅ Backend: Health, chat, session history endpoints working
- ✅ Frontend: ChatWidget renders on all documentation pages
- ✅ Frontend: User can send messages and receive responses
- ✅ Frontend: Source citations display with clickable links
- ✅ Frontend: Session persists across page reloads
- ✅ Integration: Full RAG pipeline functional (query → embedding → search → LLM → response)
- ✅ Independent Test: Acceptance scenarios 1-4 from spec.md pass

---

## Phase 4: User Story 2 - Context-Aware Follow-up Questions (P2)

**Story**: As a reader learning complex robotics concepts, I want to ask follow-up questions that reference my previous conversation, so that I can have a natural dialogue without repeating context.

**Goal**: Enable conversation context awareness (already implemented in US1 via session management)

**Duration Estimate**: 0 hours (no additional work needed)

**Independent Test**: Start conversation with "What is ROS2?", then ask "What are its main components?", verify chatbot understands "its" refers to ROS2

### Tasks

- [ ] T046 [US2] Verify conversation history is included in LLM context (check `backend/src/services/llm.py` includes last 6 messages)
- [ ] T047 [US2] Test context-aware follow-up: Ask initial question, then follow-up with pronoun reference, verify correct understanding

**Completion Criteria**:
- ✅ LLM service includes conversation history in context
- ✅ Chatbot correctly resolves pronoun references from previous messages
- ✅ Independent Test: Acceptance scenarios 1-3 from spec.md pass

**Note**: This story is largely satisfied by US1's session management and conversation history features. Only verification tasks needed.

---

## Phase 5: User Story 4 - Mobile-Friendly Chat Experience (P2)

**Story**: As a mobile user reading the documentation on my phone, I want a responsive chat interface that works well on small screens, so that I can get help even when away from my computer.

**Goal**: Make ChatWidget fully responsive for mobile devices (viewport ≤767px)

**Duration Estimate**: 2-3 hours

**Independent Test**: Open documentation on mobile device, click chat button, verify full-screen chat with properly sized touch targets

### Tasks

- [ ] T048 [P] [US4] Add mobile responsive styles to `src/theme/components/ChatWidget/styles.module.css` (viewport ≤767px: full screen, larger touch targets)
- [ ] T049 [P] [US4] Implement mobile-specific layout in ChatWindow.tsx (full screen on mobile, 400px × 600px on desktop)
- [ ] T050 [US4] Test mobile keyboard behavior: Verify virtual keyboard doesn't obscure input field
- [ ] T051 [US4] Test dark mode on mobile: Verify chat interface uses appropriate dark mode colors

**Completion Criteria**:
- ✅ Chat window expands to full screen on mobile devices
- ✅ Touch targets are appropriately sized (minimum 44px × 44px)
- ✅ Virtual keyboard doesn't obscure input field
- ✅ Dark mode works correctly on mobile
- ✅ Independent Test: Acceptance scenarios 1-4 from spec.md pass

---

## Phase 6: User Story 3 - Ask Questions About Selected Text (P3)

**Story**: As a reader who encounters confusing passages, I want to select specific text on the page and ask the chatbot to explain it in simpler terms, so that I can get targeted help on exactly what I don't understand.

**Goal**: Implement text selection feature with context banner

**Duration Estimate**: 2-3 hours

**Independent Test**: Select text on page, see yellow banner, ask "Explain this in simple terms", verify answer references selected text

### Tasks

- [ ] T052 [P] [US3] Implement TextSelection component in `src/theme/components/ChatWidget/TextSelection.tsx` (detect selection, show banner, clear button)
- [ ] T053 [US3] Add text selection event listeners to ChatWidget main component (listen for mouseup/touchend, validate length 1-1000 chars)
- [ ] T054 [US3] Update API client to include selected_text in chat requests
- [ ] T055 [US3] Style text selection banner in styles.module.css (yellow background, position above input area)
- [ ] T056 [US3] Test text selection: Select text, verify banner appears, send question, verify selected text context cleared after send
- [ ] T057 [US3] Test edge cases: Select <1 char (no banner), select >1000 chars (no banner), select different text (banner updates)

**Completion Criteria**:
- ✅ Text selection detection works on documentation pages
- ✅ Yellow banner displays with selected text preview
- ✅ Selected text included in API request
- ✅ Banner clears after message sent or X button clicked
- ✅ Edge cases handled correctly (length validation)
- ✅ Independent Test: Acceptance scenarios 1-4 from spec.md pass

---

## Phase 7: User Story 5 - Clear Loading and Error States (P3)

**Story**: As a user waiting for a chatbot response, I want clear visual feedback showing the system is working, so that I know my question was received and the system hasn't frozen.

**Goal**: Add loading indicators and error messages

**Duration Estimate**: 1-2 hours

**Independent Test**: Send question, observe animated loading indicator (three dots), simulate backend failure, verify helpful error message

### Tasks

- [ ] T058 [P] [US5] Create LoadingIndicator component in `src/theme/components/ChatWidget/LoadingIndicator.tsx` (three dots animation)
- [ ] T059 [P] [US5] Create ErrorMessage component in `src/theme/components/ChatWidget/ErrorMessage.tsx` (display error with retry button)
- [ ] T060 [US5] Add loading state to ChatWidget (show LoadingIndicator while waiting for response)
- [ ] T061 [US5] Add error handling to API client (catch network errors, display ErrorMessage)
- [ ] T062 [US5] Style loading and error states in styles.module.css (CSS animation for dots, error styling)
- [ ] T063 [US5] Test loading state: Send message, verify loading indicator appears immediately
- [ ] T064 [US5] Test error state: Disconnect backend, send message, verify error message with retry button

**Completion Criteria**:
- ✅ Loading indicator shows while waiting for responses
- ✅ Error messages display when backend unavailable
- ✅ Retry button re-attempts failed requests
- ✅ Loading state doesn't timeout/disappear prematurely
- ✅ Independent Test: Acceptance scenarios 1-4 from spec.md pass

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Final improvements, accessibility, performance optimization, documentation

**Duration Estimate**: 2-3 hours

### Accessibility

- [ ] T065 [P] Add ARIA labels to all interactive elements in ChatWidget components (aria-label for buttons, role="log" for message list)
- [ ] T066 [P] Implement keyboard navigation (Tab, Enter, Escape keys for all interactions)
- [ ] T067 [P] Add focus management (focus input when chat opens, return focus to button when closed)
- [ ] T068 [P] Verify color contrast ratios ≥4.5:1 using Chrome DevTools (check all text and borders)
- [ ] T069 Test screen reader compatibility with NVDA (Windows) or VoiceOver (Mac)

### Performance

- [ ] T070 [P] Add React.memo to MessageList component to prevent unnecessary re-renders
- [ ] T071 [P] Implement lazy loading for ChatWidget in Root.tsx (React.lazy + Suspense)
- [ ] T072 [P] Optimize CSS animations to use transform and opacity only (60fps target)
- [ ] T073 Verify bundle size <50KB using webpack-bundle-analyzer
- [ ] T074 Run Lighthouse audit: Verify FCP <1.5s, TTI <3s

### Documentation

- [ ] T075 [P] Create RAG architecture documentation at `docs/rag-architecture.md` (system diagram, data flow, deployment topology)
- [ ] T076 [P] Verify quickstart guide completeness at `specs/011-rag-chatbot-integration/quickstart.md` (test all setup steps)
- [ ] T077 [P] Add inline code comments to complex logic (RAG orchestration, prompt construction, vector search)

### Testing

- [ ] T078 [P] Write unit tests for backend services (embedding, vector_store, llm, conversation) at `backend/tests/unit/`
- [ ] T079 [P] Write integration test for RAG pipeline at `backend/tests/integration/test_rag_pipeline.py`
- [ ] T080 [P] Write API endpoint tests at `backend/tests/integration/test_api_endpoints.py`
- [ ] T081 Run pytest with coverage: `pytest backend/tests/ --cov=backend/src --cov-report=html`, verify >80% coverage

### Deployment

- [ ] T082 Deploy backend to Railway or Render (configure environment variables, verify health endpoint accessible)
- [ ] T083 Update frontend API URL in production .env to point to deployed backend
- [ ] T084 Build and deploy frontend to GitHub Pages: `npm run build && npm run deploy`
- [ ] T085 Run smoke tests on production: Test chat functionality on deployed site

**Completion Criteria**:
- ✅ All accessibility requirements met (WCAG AA compliance)
- ✅ Performance targets achieved (<3s response time, 60fps animations, <50KB bundle)
- ✅ Documentation complete (architecture, quickstart guide)
- ✅ Test coverage >80% for backend services
- ✅ Application deployed to production and verified working

---

## Parallel Execution Examples

### Example 1: Phase 2 (Foundational)

**Parallel Track A** (Developer 1):
- T010: Apply Postgres schema
- T012: Implement config.py
- T014: Implement sanitization.py

**Parallel Track B** (Developer 2):
- T011: Create Qdrant collection
- T013: Implement markdown.py
- T015: Create indexing script

**Reason**: All tasks operate on different files/services with no dependencies.

### Example 2: Phase 3 (US1 Backend)

**Parallel Track A** (Developer 1):
- T016: Create chat.py models
- T018: Implement embedding.py service
- T020: Implement llm.py service
- T024: Implement health.py endpoint

**Parallel Track B** (Developer 2):
- T017: Create document.py models
- T019: Implement vector_store.py service
- T021: Implement conversation.py service
- T026: Implement sessions.py endpoint

**Sequential After Both Complete**:
- T022: Implement rag_service.py (needs all services)
- T025: Implement chat.py endpoint (needs rag_service)

### Example 3: Phase 3 (US1 Frontend)

**Parallel Track A** (Developer 1):
- T032: ChatButton.tsx
- T034: MessageList.tsx
- T036: SourceCitation.tsx

**Parallel Track B** (Developer 2):
- T033: ChatWindow.tsx
- T035: InputArea.tsx
- T038: chatApi.ts

**Sequential After Both Complete**:
- T037: ChatWidget main component (orchestrates all)
- T039-T041: Integration and styling

---

## Task Summary

**Total Tasks**: 85
**Parallelizable Tasks**: 39 (marked with [P])

**Tasks by User Story**:
- Setup (Phase 1): 9 tasks
- Foundational (Phase 2): 6 tasks
- US1 (P1) - Core RAG: 30 tasks ⭐ MVP
- US2 (P2) - Context-aware: 2 tasks (mostly complete)
- US4 (P2) - Mobile responsive: 4 tasks
- US3 (P3) - Text selection: 6 tasks
- US5 (P3) - Loading/error states: 7 tasks
- Polish (Phase 8): 21 tasks

**Critical Path** (blocking tasks):
1. Phase 1 (Setup): T001-T009 (2-3 hours)
2. Phase 2 (Foundational): T010-T015 (1-2 hours)
3. Phase 3 (US1): T016-T045 (4-6 hours) ← **MVP Complete**

**Total MVP Time Estimate**: 7-11 hours for a fully functional RAG chatbot

**Incremental Delivery After MVP**:
- US2 (0 hours) - Already working
- US4 (2-3 hours) - Mobile support
- US3 (2-3 hours) - Text selection
- US5 (1-2 hours) - Polish
- Phase 8 (2-3 hours) - Final polish

---

## Validation Checklist

✅ **Format Validation**:
- All tasks follow `- [ ] [TaskID] [P?] [Story?] Description with file path` format
- Task IDs sequential (T001-T085)
- Story labels present for user story phases (US1-US5)
- File paths explicit in all implementation tasks

✅ **Organization Validation**:
- Tasks organized by user story for independent implementation
- Each user story has complete task set (models → services → endpoints → UI)
- Dependencies clearly marked (foundational before stories)
- Parallel opportunities identified with [P] marker

✅ **Completeness Validation**:
- Each user story has independent test criteria
- All entities from data-model.md covered
- All endpoints from contracts/api-spec.yaml covered
- All components from plan.md structure covered

✅ **Testability Validation**:
- Each user story phase includes specific test tasks
- Independent test criteria defined per story
- MVP scope clearly identified (US1)

---

## Next Steps

1. **Start with MVP**: Complete Phase 1, Phase 2, and Phase 3 (US1) for a working RAG chatbot
2. **Test MVP**: Verify US1 independent test passes before moving to other stories
3. **Incremental Delivery**: Add US2, US4, US3, US5 in order based on priority
4. **Polish**: Complete Phase 8 for production readiness

**Ready to begin implementation with `/sp.implement` command.**
