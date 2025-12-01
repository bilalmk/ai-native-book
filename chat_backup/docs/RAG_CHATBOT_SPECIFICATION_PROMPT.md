# RAG Chatbot Integration - Specification Prompt

**Purpose**: Use this prompt with `/sp.specify` to generate a complete specification for building a RAG chatbot system.

---

## Specification Request

Build a production-ready RAG (Retrieval-Augmented Generation) chatbot system that integrates with our Docusaurus documentation website to answer user questions based on the book content.

### Feature Overview

Create an intelligent chatbot that:

1. **Answers questions** about book content using semantic search and AI-generated responses
2. **Shows source citations** so users can verify information
3. **Supports text selection** allowing users to select text on the page and ask context-aware questions
4. **Maintains conversation history** across multiple messages in a session
5. **Provides a modern UI** with a floating chat button, message history, and mobile responsiveness

### Technical Requirements

#### Backend Requirements

**Technology Stack**:
- **Language**: Python 3.9+
- **Framework**: FastAPI for REST API
- **AI Provider**: OpenAI (GPT-4o-mini for chat, text-embedding-3-small for embeddings)
- **Vector Database**: Qdrant Cloud (free tier) for semantic search
- **Relational Database**: Neon Serverless Postgres (free tier) for conversation storage
- **Dependencies**: SQLAlchemy, Pydantic, python-dotenv, markdown, beautifulsoup4, tiktoken

**Core Functionality**:

1. **RAG Service** (`rag_service.py`):
   - Generate embeddings for user queries using OpenAI
   - Search for similar document chunks in Qdrant (vector similarity search)
   - Retrieve top 5 most relevant document chunks
   - Build context from retrieved chunks
   - Generate AI responses using OpenAI GPT-4o-mini with the context
   - Return answer with source citations and relevance scores

2. **Document Indexing** (`indexer.py`):
   - Read all markdown/MDX files from `docs/` directory
   - Extract frontmatter (title, sidebar_position, etc.)
   - Clean markdown content (remove code blocks, convert to plain text)
   - Chunk documents into overlapping segments (1000 words per chunk, 200-word overlap)
   - Generate embeddings for each chunk
   - Store in Qdrant with metadata (title, file_path, chunk_index, total_chunks)

3. **API Endpoints** (`main.py`):
   - `GET /api/health` - Health check returning status of all services (Qdrant, Postgres, OpenAI)
   - `POST /api/chat` - Main chat endpoint accepting {message, session_id?, selected_text?}
     - Creates or retrieves session
     - Performs semantic search
     - Generates AI response with context
     - Saves conversation to database
     - Returns {session_id, message, sources[], timestamp}
   - `GET /api/sessions/{session_id}/history` - Returns full conversation history

4. **Database Schema** (`models.py`, `database.py`):
   - **ChatSession** table: id (UUID), created_at, last_activity
   - **ChatMessage** table: id (UUID), session_id, role (user/assistant), content, selected_text, context_used, timestamp
   - Use SQLAlchemy ORM
   - Connection pooling for Neon Postgres
   - Automatic table creation on startup

5. **Configuration**:
   - Environment variables: OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, DATABASE_URL, CORS_ORIGINS
   - `.env.example` file with template
   - Docker support (Dockerfile, docker-compose.yml)

#### Frontend Requirements

**Technology Stack**:
- **Framework**: React with TypeScript
- **Integration**: Docusaurus v3+ theme swizzling
- **Styling**: CSS Modules with dark mode support
- **State Management**: React hooks (useState, useEffect, useRef)

**Core Functionality**:

1. **Chat Component** (`src/components/RAGChatbot/index.tsx`):
   - **UI Elements**:
     - Floating chat button (💬) in bottom-right corner
     - Chat window (400px × 600px) that opens on click
     - Message list with user/assistant distinction
     - Input field with send button
     - Loading indicator (animated dots)
     - Source citations with expandable details
     - Clear conversation button

   - **Features**:
     - Send messages via Enter key or button click
     - Display messages with different styles for user (purple gradient) and assistant (white/gray)
     - Show loading state while waiting for response
     - Display source citations with title, file path, and relevance percentage
     - Auto-scroll to newest message
     - Session persistence using localStorage
     - Welcome message when no conversation exists

2. **Text Selection Feature**:
   - Detect when user selects text anywhere on the documentation page
   - Show yellow banner "📝 Using selected text as context" when text is selected
   - Include selected text in API request as additional context
   - Clear selected text after message is sent or user clicks X
   - Only trigger for text selections between 1-1000 characters

3. **Styling** (`src/components/RAGChatbot/styles.module.css`):
   - Modern gradient button (purple to violet)
   - Smooth animations (slide-up, fade-in)
   - Dark mode support using `[data-theme='dark']` selectors
   - Mobile responsive (full screen on small devices)
   - Custom scrollbar styling
   - Accessibility (proper focus states, aria labels)

4. **Global Integration** (`src/theme/Root.tsx`):
   - Create Docusaurus theme wrapper component
   - Include chatbot on all pages
   - Configure API URL (hardcoded, not using process.env to avoid browser errors)
   - Render children first, then chatbot

#### Testing Requirements

Create comprehensive test suite (`test_api.py`):

1. **Health Check Test**:
   - Verify API returns 200
   - Verify status is "healthy"
   - Verify Qdrant connection is true
   - Verify database connection is true

2. **Basic Chat Test**:
   - Send message "What is Physical AI?"
   - Verify response contains comprehensive answer
   - Verify at least 3 sources returned
   - Verify relevance scores > 0.5
   - Verify session_id is returned

3. **Context-Aware Chat Test**:
   - Send initial message
   - Send follow-up message referencing previous context
   - Verify conversation memory is maintained
   - Verify response uses previous context

4. **Text Selection Test**:
   - Send message with selected_text field
   - Verify response incorporates selected text as context
   - Verify different answer than without selected text

5. **Session History Test**:
   - Create conversation with multiple messages
   - Retrieve history via GET endpoint
   - Verify all messages are returned in order
   - Verify timestamps and roles are correct

#### Documentation Requirements

1. **Backend README** (`chatbot-backend/README.md`):
   - Installation instructions
   - Environment variable setup guide
   - API endpoint documentation with examples
   - Troubleshooting section
   - Architecture diagram (ASCII art)
   - Cost breakdown
   - Deployment instructions

2. **Setup Guide** (`CHATBOT_SETUP.md`):
   - Quick start (5-minute setup)
   - Detailed step-by-step instructions
   - Prerequisites checklist
   - Service signup guides (OpenAI, Qdrant, Neon)
   - Testing instructions
   - Demo scenarios
   - Common issues and solutions

3. **Code Comments**:
   - All functions have docstrings
   - Complex logic has inline comments
   - Type hints for all function parameters and returns

### Non-Functional Requirements

#### Performance

- **Response Time**: API responses < 3 seconds (95th percentile)
  - Embedding generation: ~100ms
  - Vector search: ~50ms
  - LLM generation: ~1-2s
  - Database operations: ~50ms

- **Throughput**: Handle 10 concurrent requests
- **Frontend**: 60fps smooth animations, < 16ms render time

#### Scalability

- Support 1000+ indexed documents
- Handle 10,000+ vectors in Qdrant
- Manage 100+ concurrent sessions
- Database connection pooling (5-10 connections)

#### Reliability

- 95%+ uptime
- Graceful error handling (no crashes)
- Automatic retry for transient failures
- Database transaction rollback on errors
- Fallback messages when services are unavailable

#### Security

- API keys stored in environment variables (never in code)
- CORS properly configured for allowed origins only
- Input validation using Pydantic models
- SQL injection prevention via ORM
- XSS prevention in frontend
- No sensitive data in logs

#### Cost Efficiency

- Monthly operating cost: $5-10 for moderate usage (1000 queries/month)
- OpenAI: ~$5-10 (embeddings + chat completions)
- Qdrant: $0 (free tier, 1GB storage)
- Neon Postgres: $0 (free tier, 0.5GB storage)
- Token optimization (limit context length, efficient prompts)

#### Maintainability

- Clean code structure with separation of concerns
- Type safety (Pydantic models, TypeScript interfaces)
- Comprehensive error messages
- Logging for debugging
- Configuration via environment variables
- Docker support for consistent deployment

#### Usability

- **User Experience**:
  - Intuitive chat interface
  - Clear loading states
  - Helpful error messages
  - Keyboard shortcuts (Enter to send)
  - Mobile-friendly design
  - Accessibility (ARIA labels, keyboard navigation)

- **Developer Experience**:
  - Clear documentation
  - Easy local setup (< 10 minutes)
  - Comprehensive tests
  - Example usage
  - Troubleshooting guide

### Constraints

1. **Technology Constraints**:
   - Must use OpenAI (no other LLM providers)
   - Must use Qdrant Cloud (no local Qdrant)
   - Must use Neon Postgres (no other databases)
   - Must integrate with existing Docusaurus site
   - Must work in WSL/Linux and Windows environments

2. **Budget Constraints**:
   - Total monthly cost < $15
   - Use free tiers where possible
   - Optimize token usage

3. **Time Constraints**:
   - Backend setup: < 2 hours
   - Frontend integration: < 1 hour
   - Testing: < 30 minutes
   - Documentation: < 1 hour

4. **Integration Constraints**:
   - Must not break existing Docusaurus functionality
   - Must not require Docusaurus configuration changes
   - Should work with existing content structure
   - No modifications to existing documentation files

### Success Criteria

The implementation will be considered successful when:

1. **Functional Completeness**:
   - ✅ All 5 test cases pass (health, basic chat, context, text selection, history)
   - ✅ Chat button appears on all documentation pages
   - ✅ Users can ask questions and receive relevant answers
   - ✅ Source citations are displayed with every answer
   - ✅ Text selection feature works correctly
   - ✅ Conversation history persists across page reloads

2. **Quality Standards**:
   - ✅ Average relevance score > 70% for top result
   - ✅ Response time < 3 seconds for 95% of queries
   - ✅ Error rate < 5%
   - ✅ Zero crashes or unhandled exceptions
   - ✅ All TypeScript/Python code is type-safe

3. **User Experience**:
   - ✅ Chat interface is intuitive and requires no instructions
   - ✅ Mobile users can use the chatbot effectively
   - ✅ Dark mode works correctly
   - ✅ Loading states are clear and professional
   - ✅ Error messages are helpful and actionable

4. **Documentation**:
   - ✅ README includes all necessary setup steps
   - ✅ Environment variables are documented
   - ✅ API endpoints are documented with examples
   - ✅ Troubleshooting guide covers common issues
   - ✅ Code has comprehensive comments

5. **Deployment Readiness**:
   - ✅ Backend can be deployed to Railway/Render
   - ✅ Frontend works with production builds
   - ✅ Environment variables work in production
   - ✅ CORS is configured for production domain
   - ✅ Health check endpoint returns correct status

### Out of Scope

The following are explicitly excluded from this implementation:

❌ **Not Included**:
- Voice input/output
- Multi-language support
- User authentication/accounts
- Conversation sharing/export
- Admin dashboard
- Analytics/metrics UI
- Rate limiting
- Caching layer
- Custom LLM fine-tuning
- Feedback collection UI
- Search history
- Suggested questions
- Multi-modal input (images, files)

These features may be added in future iterations but are not required for the initial release.

### Example Interactions

#### Example 1: Basic Question
**User**: "What is Physical AI?"
**Expected**:
- Response time: ~2 seconds
- Answer: 3-4 paragraphs explaining Physical AI, embodied intelligence, perception-action loop
- Sources: 3 citations from relevant documentation pages
- Relevance: Top source > 70%

#### Example 2: Text Selection
**User selects**: "Embodied intelligence is built upon a continuous cycle of three interconnected components: perception, cognition, and action."
**User asks**: "Explain this in simple terms"
**Expected**:
- Yellow banner showing "Using selected text as context"
- Response uses the selected text to provide a simplified explanation
- Answer mentions the three components specifically
- Sources cite the same page where text was selected

#### Example 3: Follow-up Question
**User**: "What is ROS2?"
**Bot**: [Explains ROS2]
**User**: "What are its main components?"
**Expected**:
- Bot understands "its" refers to ROS2
- Answer lists ROS2 components (nodes, topics, services, actions)
- Conversation context is maintained

#### Example 4: No Relevant Content
**User**: "What is the weather today?"
**Expected**:
- Bot responds: "I don't have information about that in the documentation. I can only answer questions about Physical AI, robotics, ROS2, and related topics covered in this book."
- No hallucinated information
- Helpful guidance on what questions can be answered

### Acceptance Criteria Checklist

Use this checklist to verify implementation completeness:

**Backend**:
- [ ] FastAPI server starts without errors
- [ ] All environment variables are documented
- [ ] Health endpoint returns correct status
- [ ] Chat endpoint accepts and validates requests
- [ ] RAG service generates embeddings
- [ ] Vector search returns relevant results
- [ ] LLM generates accurate responses
- [ ] Database stores conversations
- [ ] Session management works correctly
- [ ] CORS is configured properly
- [ ] Error handling is comprehensive
- [ ] All tests pass (5/5)

**Frontend**:
- [ ] Chat button renders on all pages
- [ ] Chat window opens and closes
- [ ] Messages display correctly
- [ ] User can send messages
- [ ] Loading state shows while waiting
- [ ] Assistant responses display
- [ ] Source citations appear
- [ ] Text selection detection works
- [ ] Selected text banner shows
- [ ] Conversation persists in session
- [ ] Mobile responsive design works
- [ ] Dark mode styles apply
- [ ] No console errors

**Documentation**:
- [ ] README is complete and accurate
- [ ] Setup guide has step-by-step instructions
- [ ] Environment variables are documented
- [ ] API endpoints are documented
- [ ] Troubleshooting section exists
- [ ] Code has comments
- [ ] Examples are provided

**Deployment**:
- [ ] Backend deploys to cloud platform
- [ ] Frontend builds successfully
- [ ] Production environment variables work
- [ ] CORS configured for production
- [ ] Health check accessible
- [ ] End-to-end test passes in production

### Reference Implementation

This specification is based on a working implementation with the following verified metrics:

- **Total Files Created**: 15 (12 backend, 3 frontend)
- **Lines of Code**: ~2500 (Python: ~1500, TypeScript: ~1000)
- **Test Coverage**: 100% (5/5 tests passing)
- **Response Time**: 1.5-2.5 seconds average
- **Relevance Score**: 55-75% for top results
- **Cost**: $5-10/month for 1000 queries
- **Setup Time**: 10 minutes (excluding service signups)
- **Deployment Time**: 15 minutes

### Technical Specifications Summary

| Component | Specification |
|-----------|--------------|
| **Backend Language** | Python 3.9+ |
| **Backend Framework** | FastAPI 0.115.0 |
| **Frontend** | React + TypeScript |
| **LLM Model** | GPT-4o-mini |
| **Embedding Model** | text-embedding-3-small (1536 dim) |
| **Vector DB** | Qdrant Cloud |
| **Database** | Neon Serverless Postgres |
| **Chunk Size** | 1000 words |
| **Chunk Overlap** | 200 words |
| **Retrieval Limit** | 5 documents |
| **Max Tokens** | 1000 for responses |
| **Temperature** | 0.7 |
| **Session Timeout** | 7 days |
| **CORS Origins** | Configurable via environment |

---

## Usage Instructions

**To generate specification using this prompt:**

```bash
/sp.specify
```

Then paste this entire prompt when asked for the feature description.

The specification will be generated and saved in:
- `specs/[feature-name]/spec.md`
- Related checklists, data models, and research artifacts

**Next steps after specification:**
1. Review the generated spec
2. Run `/sp.plan` to create implementation plan
3. Run `/sp.tasks` to generate actionable tasks
4. Run `/sp.implement` to execute implementation

---

**Version**: 1.0.0
**Last Updated**: 2025-12-01
**Status**: Production-Ready Reference
