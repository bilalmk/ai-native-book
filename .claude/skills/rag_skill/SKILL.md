# RAG Chatbot Integration Skill

**Purpose**: Build and integrate production-ready RAG (Retrieval-Augmented Generation) chatbots into documentation sites using OpenAI, Qdrant Cloud, and Neon Postgres.

## Skill Overview

This skill provides comprehensive knowledge and templates for building intelligent chatbots that can answer questions based on documentation content using RAG architecture. It includes backend API development, vector database integration, conversation management, and frontend UI components.

## When to Use This Skill

Use this skill when you need to:
- Add an AI-powered Q&A chatbot to documentation sites
- Implement semantic search over documentation content
- Build conversational interfaces with source citations
- Create context-aware chatbots with text selection features
- Integrate OpenAI, Qdrant, and PostgreSQL for RAG systems

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **LLM Provider**: OpenAI (GPT-4o-mini, text-embedding-3-small)
- **Vector Database**: Qdrant Cloud (free tier available)
- **Relational Database**: Neon Serverless Postgres (free tier available)
- **Additional Libraries**: SQLAlchemy, Pydantic, python-dotenv

### Frontend
- **Framework**: React + TypeScript
- **Integration**: Docusaurus v3+
- **Styling**: CSS Modules with dark mode support
- **Features**: Text selection, session management, source citations

## Architecture Components

### 1. Backend API Structure

```
chatbot-backend/
├── main.py              # FastAPI application with endpoints
├── rag_service.py       # RAG logic (embeddings + retrieval + generation)
├── database.py          # Database connection and session management
├── models.py            # Pydantic and SQLAlchemy models
├── indexer.py           # Document indexing script
├── test_api.py          # Comprehensive test suite
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── Dockerfile           # Container configuration
└── docker-compose.yml   # Multi-service orchestration
```

### 2. Core API Endpoints

**Health Check**: `GET /api/health`
- Returns system status and service connectivity

**Chat**: `POST /api/chat`
- Input: `{message, session_id?, selected_text?}`
- Output: `{session_id, message, sources[], timestamp}`

**Session History**: `GET /api/sessions/{session_id}/history`
- Returns full conversation history for a session

### 3. Frontend Components

```
book/src/
├── components/
│   └── RAGChatbot/
│       ├── index.tsx           # Main chat component
│       └── styles.module.css   # Component styles
└── theme/
    └── Root.tsx                # Global wrapper for chatbot
```

## Implementation Pattern

### Phase 1: Backend Setup

1. **Create Project Structure**
   ```bash
   mkdir chatbot-backend
   cd chatbot-backend
   ```

2. **Configure Environment Variables**
   - OpenAI API key
   - Qdrant Cloud URL and API key
   - Neon Postgres connection string
   - CORS origins

3. **Implement Core Services**
   - RAG service with embedding generation
   - Vector similarity search
   - LLM response generation with context
   - Database session management

4. **Create Indexing Pipeline**
   - Extract content from markdown/MDX files
   - Clean and chunk documents
   - Generate embeddings
   - Store in Qdrant with metadata

### Phase 2: Frontend Integration

1. **Create Chat Component**
   - Message display with user/assistant roles
   - Loading states and animations
   - Source citation display
   - Error handling

2. **Implement Text Selection Feature**
   - Detect text selection on page
   - Show context indicator
   - Include selected text in API requests

3. **Add Global Integration**
   - Create Root.tsx wrapper
   - Configure API endpoint
   - Enable CORS

### Phase 3: Testing & Deployment

1. **Run Test Suite**
   - Health checks
   - Basic Q&A
   - Context-aware queries
   - Session management
   - Text selection

2. **Deploy Services**
   - Backend: Railway, Render, or AWS
   - Frontend: GitHub Pages or Vercel
   - Update CORS and API URLs

## Key Features

### 1. RAG-Powered Responses
```python
# Semantic search in Qdrant
query_embedding = get_embedding(user_query)
similar_docs = qdrant.search(query_embedding, limit=5)

# Generate response with context
context = build_context(similar_docs)
response = openai.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_query}"}
    ]
)
```

### 2. Text Selection Context
```typescript
// Detect text selection
useEffect(() => {
  const handleSelection = () => {
    const selection = window.getSelection();
    const text = selection?.toString().trim();
    if (text && text.length > 0) {
      setSelectedText(text);
    }
  };

  document.addEventListener('mouseup', handleSelection);
}, []);
```

### 3. Conversation Memory
```python
# Store chat history in Postgres
chat_history = db.query(ChatMessage).filter(
    ChatMessage.session_id == session.id
).order_by(ChatMessage.timestamp.desc()).limit(10).all()

# Include in LLM context
history_messages = [
    {"role": msg.role, "content": msg.content}
    for msg in reversed(chat_history)
]
```

### 4. Source Citations
```python
# Return sources with relevance scores
sources = [
    {
        "title": doc["title"],
        "file_path": doc["file_path"],
        "score": round(doc["score"], 3)
    }
    for doc in context_docs[:3]
]
```

## Document Indexing Strategy

### Chunking Parameters
- **Chunk Size**: 1000 words (adjustable)
- **Overlap**: 200 words (for context continuity)
- **Metadata**: Title, file path, chunk index, sidebar position

### Embedding Model
- **Model**: text-embedding-3-small (1536 dimensions)
- **Cost**: ~$0.00002 per 1K tokens
- **Performance**: ~100ms per embedding

### Vector Search
- **Distance Metric**: Cosine similarity
- **Results**: Top 5 most relevant chunks
- **Threshold**: Minimum 0.5 similarity score

## Environment Configuration

### Required Services

1. **OpenAI Account**
   - API key from platform.openai.com
   - Billing enabled
   - ~$5-10/month for moderate usage

2. **Qdrant Cloud**
   - Free tier: 1GB storage
   - Create cluster at cloud.qdrant.io
   - Copy cluster URL and API key

3. **Neon Postgres**
   - Free tier: 0.5GB storage, 100 hours compute
   - Create database at neon.tech
   - Copy connection string

### Environment Variables Template
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-...

# Qdrant Configuration
QDRANT_URL=https://xxx.cloud.qdrant.io:6333
QDRANT_API_KEY=...
QDRANT_COLLECTION_NAME=ai_native_book

# Neon Postgres Configuration
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

# Application Settings
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,https://your-domain.com
```

## Dependencies

### Backend (requirements.txt)
```
fastapi==0.115.0
uvicorn[standard]==0.32.0
python-dotenv==1.0.1
openai==1.54.0
qdrant-client==1.12.0
psycopg2-binary==2.9.10
sqlalchemy==2.0.35
pydantic==2.9.2
pydantic-settings==2.6.0
python-multipart==0.0.12
markdown==3.7
beautifulsoup4==4.12.3
tiktoken==0.8.0
```

### Frontend
No additional dependencies required (uses existing Docusaurus setup)

## Testing Strategy

### Test Coverage Areas
1. **Health Checks**: Verify all services connected
2. **Basic Q&A**: Test RAG retrieval and generation
3. **Context Awareness**: Test conversation memory
4. **Text Selection**: Test selected text integration
5. **Session Management**: Test database persistence

### Sample Test Script
```python
import requests

# Test health
response = requests.get("http://localhost:8000/api/health")
assert response.json()["status"] == "healthy"

# Test chat
response = requests.post(
    "http://localhost:8000/api/chat",
    json={"message": "What is Physical AI?"}
)
assert "session_id" in response.json()
assert len(response.json()["sources"]) > 0
```

## Performance Metrics

### Expected Response Times
- **Embedding Generation**: ~100ms
- **Vector Search**: ~50ms
- **LLM Generation**: ~1-2 seconds
- **Database Operations**: ~50ms
- **Total Response**: ~1.5-2.5 seconds

### Accuracy Metrics
- **Relevance Scores**: 55-75% for top results
- **Context Retrieval**: 3-5 relevant chunks per query
- **Answer Quality**: High when relevant context is found

## Common Issues & Solutions

### Issue: "process is not defined" in browser
**Solution**: Don't use `process.env` in React components. Use hardcoded values or build-time environment variables.

```typescript
// ❌ Wrong
<RAGChatbot apiUrl={process.env.REACT_APP_API_URL} />

// ✅ Correct
<RAGChatbot apiUrl="http://localhost:8000" />
```

### Issue: OpenAI client initialization error
**Solution**: Upgrade to latest OpenAI SDK version
```bash
pip install --upgrade openai
```

### Issue: Empty search results
**Solution**: Ensure documents are indexed
```bash
python indexer.py
```

### Issue: CORS errors
**Solution**: Configure CORS origins in backend
```python
CORS_ORIGINS=http://localhost:3000,https://production-domain.com
```

## Deployment Checklist

- [ ] Backend deployed to Railway/Render
- [ ] Environment variables configured in production
- [ ] Documents indexed in Qdrant
- [ ] Database tables created in Neon
- [ ] CORS configured for production domain
- [ ] Frontend API URL updated
- [ ] Health check endpoint returning success
- [ ] Test suite passing
- [ ] Monitoring/logging configured

## Cost Estimation

**Monthly costs (moderate usage - 1000 queries):**
- OpenAI: $5-10 (embeddings + GPT-4)
- Qdrant Cloud: $0 (free tier)
- Neon Postgres: $0 (free tier)
- **Total**: $5-10/month

## Success Criteria

✅ User asks question → Gets relevant answer
✅ User selects text → Context indicator appears
✅ Follow-up questions → Conversation memory works
✅ Sources shown → User can verify information
✅ Response time → Under 3 seconds
✅ Relevance → Top source > 70% similarity

## Example Usage Workflow

1. **User opens documentation** → Chat button appears
2. **User asks "What is Physical AI?"** → Backend searches Qdrant
3. **System finds 5 relevant chunks** → Combines with query
4. **OpenAI generates answer** → Returns with source citations
5. **User sees answer + sources** → Can verify information
6. **User selects text on page** → Yellow banner appears
7. **User asks "Explain this"** → Context-aware response
8. **Conversation continues** → Memory maintained

## Next Steps After Implementation

1. Monitor usage and costs
2. Tune chunk size and retrieval parameters
3. Add more advanced features (multi-language, voice input)
4. Implement analytics and feedback collection
5. Optimize response time and quality
6. Scale infrastructure as needed

---

**Version**: 1.0.0
**Last Updated**: 2025-12-01
**Tested With**: Docusaurus 3.9.2, OpenAI API v2.8.1, Qdrant 1.12.0
