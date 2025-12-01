# RAG Chatbot Backend

A FastAPI-based RAG (Retrieval-Augmented Generation) chatbot backend for the AI Native Development book.

## Features

- **RAG-powered Q&A**: Uses OpenAI embeddings and GPT-4 to answer questions based on book content
- **Vector Search**: Qdrant Cloud integration for semantic search
- **Chat History**: Neon Serverless Postgres for persistent conversations
- **Context-Aware**: Supports text selection for context-specific queries
- **REST API**: Clean FastAPI endpoints with automatic documentation

## Prerequisites

1. **Python 3.9+**
2. **OpenAI API Key** - Get from [OpenAI Platform](https://platform.openai.com/)
3. **Qdrant Cloud Account** - Free tier available at [Qdrant Cloud](https://cloud.qdrant.io/)
4. **Neon Postgres Database** - Free tier available at [Neon](https://neon.tech/)

## Setup Instructions

### 1. Install Dependencies

```bash
cd chatbot-backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-...your-key-here

# Qdrant Configuration (from Qdrant Cloud)
QDRANT_URL=https://xyz-example.eu-central.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=ai_native_book

# Neon Postgres Configuration
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# Application Settings
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,https://bilalmk.github.io
```

### 3. Index Book Content

Run the indexer to populate the vector database:

```bash
python indexer.py
```

This will:
- Read all markdown/mdx files from `../book/docs/`
- Extract and clean content
- Generate embeddings using OpenAI
- Store in Qdrant with metadata

Expected output:
```
Indexing documents from: /path/to/book/docs
Found 28 files to index
Indexing: docs/physical-ai/01-foundations-of-physical-ai.mdx#chunk0
✓ Indexed 01-foundations-of-physical-ai.mdx (5 chunks)
...
✓ Indexing complete! Indexed 28 files
```

### 4. Start the Server

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

### 5. Verify Installation

Visit the API documentation:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health

Expected health check response:
```json
{
  "status": "healthy",
  "qdrant_connected": true,
  "database_connected": true,
  "timestamp": "2025-12-01T12:00:00"
}
```

## API Endpoints

### Chat Endpoint

**POST** `/api/chat`

Request:
```json
{
  "session_id": "optional-uuid",
  "message": "What is Physical AI?",
  "selected_text": "optional text selected by user"
}
```

Response:
```json
{
  "session_id": "uuid",
  "message": "Physical AI refers to...",
  "sources": [
    {
      "title": "Foundations of Physical AI",
      "file_path": "docs/physical-ai/01-foundations-of-physical-ai.mdx",
      "score": 0.892
    }
  ],
  "timestamp": "2025-12-01T12:00:00"
}
```

### Get Chat History

**GET** `/api/sessions/{session_id}/history`

Returns all messages for a session.

### Health Check

**GET** `/api/health`

Returns system health status.

## How It Works

1. **User Query** → Backend receives question (optionally with selected text)
2. **Embedding Generation** → Query converted to vector using OpenAI embeddings
3. **Semantic Search** → Qdrant finds most relevant book sections
4. **Context Building** → Retrieved content combined with query
5. **LLM Response** → OpenAI GPT generates answer based on context
6. **History Storage** → Conversation saved to Neon Postgres
7. **Response** → Answer returned with source citations

## Architecture

```
┌─────────────┐
│   Frontend  │ (Docusaurus + React)
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   FastAPI   │ (main.py)
└──────┬──────┘
       │
       ├─────────► ┌──────────────┐
       │           │   OpenAI     │ (Embeddings + GPT)
       │           └──────────────┘
       │
       ├─────────► ┌──────────────┐
       │           │   Qdrant     │ (Vector Search)
       │           └──────────────┘
       │
       └─────────► ┌──────────────┐
                   │    Neon      │ (Chat History)
                   └──────────────┘
```

## Testing

### Test with curl

```bash
# Health check
curl http://localhost:8000/api/health

# Send a chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Physical AI?"
  }'

# Chat with selected text context
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain this in simple terms",
    "selected_text": "Embodied intelligence is built upon..."
  }'
```

### Test with Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "message": "What is Physical AI?",
    }
)

print(response.json())
```

## Troubleshooting

### Database Connection Error

If you see `DATABASE_URL environment variable is not set`:
1. Ensure `.env` file exists in `chatbot-backend/`
2. Verify DATABASE_URL format is correct
3. Check Neon dashboard for connection string

### Qdrant Connection Error

If Qdrant connection fails:
1. Verify QDRANT_URL includes port `:6333`
2. Check API key is correct
3. Ensure cluster is running in Qdrant Cloud dashboard

### OpenAI API Error

If you get 401 Unauthorized:
1. Verify OPENAI_API_KEY is valid
2. Check you have credits in OpenAI account
3. Ensure API key has proper permissions

### No Results from Search

If semantic search returns empty:
1. Run `python indexer.py` to index documents
2. Check Qdrant dashboard to verify collection exists
3. Verify documents were indexed successfully

## Development

### Run in Development Mode

```bash
uvicorn main:app --reload
```

Auto-reloads on code changes.

### Re-index Documents

After updating book content:

```bash
python indexer.py
```

### Clear Chat History

Connect to Neon Postgres and run:

```sql
TRUNCATE TABLE chat_messages;
TRUNCATE TABLE chat_sessions;
```

## Production Deployment

### Environment Variables

Set in production:
```env
ENVIRONMENT=production
CORS_ORIGINS=https://bilalmk.github.io
```

### Run with Gunicorn

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Deploy Options

- **Railway**: Easy deployment with auto-scaling
- **Render**: Free tier available
- **Fly.io**: Global edge deployment
- **AWS Lambda**: Serverless with Mangum adapter

## Cost Estimation

With moderate usage (~1000 queries/month):

- **OpenAI**: ~$5-10/month (embeddings + GPT-4)
- **Qdrant Cloud**: Free tier (up to 1GB)
- **Neon Postgres**: Free tier (0.5GB storage)

**Total**: $5-10/month on free tiers of Qdrant and Neon

## License

MIT
