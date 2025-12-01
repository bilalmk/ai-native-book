# RAG Chatbot Integration - Complete Setup Guide

This guide walks you through setting up the integrated RAG chatbot for the AI Native Development book.

## Overview

The chatbot system consists of:

1. **Backend API** (FastAPI) - Handles RAG queries and chat history
2. **Vector Database** (Qdrant Cloud) - Stores document embeddings
3. **Relational Database** (Neon Postgres) - Stores chat sessions
4. **Frontend Component** (React) - Embedded in Docusaurus

## Quick Start (5 Minutes)

### Prerequisites

- Python 3.9+
- Node.js 20+
- OpenAI API key
- Qdrant Cloud account (free)
- Neon Postgres database (free)

### Step 1: Clone and Setup Backend

```bash
cd chatbot-backend

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### Step 2: Configure Services

#### Get OpenAI API Key

1. Visit https://platform.openai.com/api-keys
2. Create new secret key
3. Copy to `.env` as `OPENAI_API_KEY`

#### Setup Qdrant Cloud

1. Visit https://cloud.qdrant.io/
2. Create free cluster
3. Copy cluster URL and API key to `.env`:
   ```env
   QDRANT_URL=https://xxx.cloud.qdrant.io:6333
   QDRANT_API_KEY=your-key-here
   ```

#### Setup Neon Postgres

1. Visit https://neon.tech/
2. Create new project
3. Copy connection string to `.env`:
   ```env
   DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
   ```

### Step 3: Index Book Content

```bash
# From chatbot-backend directory
python indexer.py
```

Expected output:
```
Indexing documents from: /path/to/book/docs
Found 28 files to index
✓ Indexed 01-foundations-of-physical-ai.mdx (5 chunks)
...
✓ Indexing complete! Indexed 28 files
```

### Step 4: Start Backend

```bash
python main.py
```

Server runs at http://localhost:8000

Verify at http://localhost:8000/docs

### Step 5: Test Backend

```bash
# In new terminal
python test_api.py
```

Should see all tests passing:
```
✓ PASS - Health Check
✓ PASS - Basic Chat
✓ PASS - Context-Aware Chat
✓ PASS - Session History
✓ PASS - Selected Text Chat

Results: 5/5 tests passed (100%)
```

### Step 6: Start Frontend

```bash
cd ../book
npm start
```

Visit http://localhost:3000

The chatbot icon (💬) appears in bottom-right corner!

## Features

### 1. Basic Q&A

Click the chat icon and ask questions:
- "What is Physical AI?"
- "Explain the perception-action loop"
- "What are the key components of ROS2?"

The chatbot retrieves relevant sections and generates answers.

### 2. Text Selection Feature

1. Select any text on the page
2. Yellow banner appears: "📝 Using selected text as context"
3. Ask follow-up questions like:
   - "Explain this in simple terms"
   - "Give me an example"
   - "How does this work?"

The chatbot uses selected text as additional context!

### 3. Conversation History

The chatbot remembers your conversation:
- Follow-up questions work naturally
- Context maintained across messages
- Session persists until cleared

### 4. Source Citations

Every answer includes sources:
- Section titles
- File paths
- Relevance scores

Click sources to verify information.

## Architecture

```
┌─────────────────────────────────────────┐
│         Docusaurus Frontend             │
│  ┌───────────────────────────────────┐  │
│  │   RAGChatbot Component            │  │
│  │   - Chat UI                       │  │
│  │   - Text selection detection      │  │
│  │   - Message history               │  │
│  └──────────────┬────────────────────┘  │
│                 │ HTTP POST              │
└─────────────────┼────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend                 │
│  ┌───────────────────────────────────┐  │
│  │   /api/chat endpoint              │  │
│  │   - Session management            │  │
│  │   - RAG orchestration             │  │
│  └──────────────┬────────────────────┘  │
└─────────────────┼────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌──────────────┐    ┌──────────────┐
│   OpenAI     │    │   Qdrant     │
│              │    │              │
│ - Embeddings │    │ - Vector DB  │
│ - GPT-4      │    │ - Semantic   │
│              │    │   Search     │
└──────────────┘    └──────────────┘
        │
        ▼
┌──────────────┐
│    Neon      │
│              │
│ - Chat       │
│   History    │
│ - Sessions   │
└──────────────┘
```

## File Structure

```
ai-native-book/
├── chatbot-backend/
│   ├── main.py                 # FastAPI app
│   ├── rag_service.py          # RAG logic
│   ├── database.py             # Postgres connection
│   ├── models.py               # Data models
│   ├── indexer.py              # Document indexing
│   ├── test_api.py             # Test suite
│   ├── requirements.txt        # Python deps
│   ├── .env                    # Config (create from .env.example)
│   └── README.md               # Backend docs
│
└── book/
    ├── src/
    │   ├── components/
    │   │   └── RAGChatbot/
    │   │       ├── index.tsx           # Chat component
    │   │       └── styles.module.css   # Styles
    │   └── theme/
    │       └── Root.tsx                # Global wrapper
    └── docs/                           # Book content (indexed)
```

## API Reference

### POST /api/chat

Send a chat message.

**Request:**
```json
{
  "session_id": "uuid-optional",
  "message": "What is Physical AI?",
  "selected_text": "optional selected text"
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "message": "Physical AI refers to...",
  "sources": [
    {
      "title": "Foundations of Physical AI",
      "file_path": "docs/physical-ai/01-foundations.mdx",
      "score": 0.89
    }
  ],
  "timestamp": "2025-12-01T12:00:00"
}
```

### GET /api/sessions/{session_id}/history

Get conversation history.

**Response:**
```json
{
  "session_id": "uuid",
  "messages": [
    {
      "role": "user",
      "content": "What is Physical AI?",
      "timestamp": "2025-12-01T12:00:00"
    },
    {
      "role": "assistant",
      "content": "Physical AI refers to...",
      "timestamp": "2025-12-01T12:00:01"
    }
  ]
}
```

### GET /api/health

Check system health.

**Response:**
```json
{
  "status": "healthy",
  "qdrant_connected": true,
  "database_connected": true,
  "timestamp": "2025-12-01T12:00:00"
}
```

## Troubleshooting

### Backend won't start

**Error:** `DATABASE_URL environment variable is not set`

**Solution:** Create `.env` file in `chatbot-backend/` from `.env.example`

---

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Install requirements:
```bash
pip install -r requirements.txt
```

### Indexing fails

**Error:** `Qdrant connection failed`

**Solution:**
1. Verify QDRANT_URL includes port `:6333`
2. Check API key in Qdrant dashboard
3. Ensure cluster is running

### No chat responses

**Error:** Chat sends but no response

**Solution:**
1. Check backend is running: http://localhost:8000/api/health
2. Check browser console for CORS errors
3. Verify `CORS_ORIGINS` in `.env` includes frontend URL

### Empty search results

**Error:** "I don't have information about that"

**Solution:**
1. Run indexer: `python indexer.py`
2. Verify in Qdrant dashboard that collection exists
3. Check collection has points (vectors)

## Production Deployment

### Backend Deployment

**Recommended: Railway**

1. Create Railway account
2. Create new project from GitHub repo
3. Add environment variables in Railway dashboard
4. Deploy automatically on push

**Alternative: Render**

1. Create Render account
2. New Web Service from GitHub
3. Build command: `pip install -r chatbot-backend/requirements.txt`
4. Start command: `cd chatbot-backend && gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`

### Frontend Deployment

The chatbot is already integrated! Just:

1. Update `apiUrl` in `book/src/theme/Root.tsx`:
   ```tsx
   <RAGChatbot apiUrl="https://your-backend.railway.app" />
   ```

2. Deploy Docusaurus normally:
   ```bash
   npm run build
   npm run deploy
   ```

### Environment Variables for Production

```env
ENVIRONMENT=production
CORS_ORIGINS=https://bilalmk.github.io,https://your-domain.com
```

## Cost Breakdown

**Monthly costs (moderate usage - 1000 queries):**

| Service | Tier | Cost |
|---------|------|------|
| OpenAI | Pay-as-go | $5-10 |
| Qdrant Cloud | Free tier | $0 |
| Neon Postgres | Free tier | $0 |
| **Total** | | **$5-10** |

**Free tiers include:**
- Qdrant: 1GB storage
- Neon: 0.5GB storage, 100 hours compute

## Advanced Configuration

### Customize Chat Model

Edit `chatbot-backend/rag_service.py`:

```python
self.chat_model = "gpt-4o"  # Use GPT-4 for better quality
```

### Adjust Search Results

Edit `chatbot-backend/rag_service.py`:

```python
# Return more context documents
context_docs = rag_service.search_similar(search_query, limit=10)
```

### Chunk Size Optimization

Edit `chatbot-backend/indexer.py`:

```python
# Larger chunks for more context
chunks = self.chunk_document(clean_content, chunk_size=2000, overlap=400)
```

### Change Chatbot Position

Edit `book/src/components/RAGChatbot/styles.module.css`:

```css
.chatbotContainer {
  bottom: 20px;
  left: 20px;  /* Move to left side */
}
```

## Testing

### Manual Testing

1. **Health Check:**
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **Simple Query:**
   ```bash
   curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What is Physical AI?"}'
   ```

3. **With Selected Text:**
   ```bash
   curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Explain this",
       "selected_text": "Embodied intelligence..."
     }'
   ```

### Automated Testing

Run full test suite:
```bash
cd chatbot-backend
python test_api.py
```

### Frontend Testing

1. Open http://localhost:3000
2. Click chat icon (💬)
3. Test features:
   - Send message
   - Select text on page
   - Ask follow-up questions
   - Check sources
   - Clear conversation

## Support

**Backend Issues:** See `chatbot-backend/README.md`

**API Documentation:** http://localhost:8000/docs

**Component Issues:** Check browser console

## Next Steps

1. ✓ Backend running
2. ✓ Content indexed
3. ✓ Frontend integrated
4. ✓ Tests passing

**Now you can:**
- Ask questions about the book
- Select text for context-aware queries
- Have natural conversations
- Get source citations

**Deploy to production:**
- Deploy backend to Railway/Render
- Update API URL in frontend
- Deploy Docusaurus site

Enjoy your intelligent book assistant! 🚀
