# Backend Setup Guide

Quick setup guide for the RAG chatbot backend.

## Prerequisites

- Python 3.9+ (you have 3.12.3 ✓)
- OpenAI API key
- Qdrant Cloud account (free tier)
- Neon Postgres database (free tier)

## Step 1: Install System Dependencies

```bash
sudo apt update && sudo apt install -y python3.12-venv python3-pip
```

## Step 2: Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Or using the pyproject.toml:**
```bash
pip install -e .
```

## Step 4: Configure Environment Variables

Copy the example file and add your real credentials:

```bash
cp .env.example .env
```

Then edit `.env` and replace the placeholder values with your actual credentials:
- OpenAI API key from https://platform.openai.com/api-keys
- Qdrant URL and API key from your Qdrant Cloud dashboard
- Neon Postgres database URL from your Neon console

## Step 5: Apply Database Schema

Connect to your Neon database using the connection string from your `.env` file:

```bash
psql "$DATABASE_URL"
```

Then paste the contents of:
`../specs/011-rag-chatbot-integration/contracts/database-schema.sql`

**Or run it directly:**
```bash
psql "$DATABASE_URL" < ../specs/011-rag-chatbot-integration/contracts/database-schema.sql
```

## Step 6: Index Documentation

```bash
python scripts/index_docs.py --docs-dir ../book/docs
```

Expected output:
```
INFO - Found 50+ markdown files
INFO - Processing file.md: 3 chunks
...
INFO - Indexing complete: 50 files, 150+ chunks
```

## Step 7: Start Backend Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs (Swagger UI)
- Health: http://localhost:8000/api/health

## Step 8: Test Backend

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Expected response:
# {"status":"healthy","services":{"qdrant":"up","postgres":"up","openai":"up"}}
```

```bash
# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?"}'
```

## Step 9: Start Frontend

In a new terminal:
```bash
cd ../book
npm install  # If dependencies not installed
npm run start
```

The site will open at http://localhost:3000

## Step 10: Test Chatbot

1. Open http://localhost:3000
2. Click the chat button (💬) in the bottom-right corner
3. Ask: "What is Physical AI?"
4. Verify you get a response with 3+ source citations

## Troubleshooting

### Import Errors
If you see `ModuleNotFoundError`, make sure you're in the virtual environment:
```bash
source venv/bin/activate
```

### Qdrant Connection Failed
- Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Run indexing script to populate the collection

### Postgres Connection Failed
- Verify `DATABASE_URL` in `.env`
- Ensure database schema is applied

### OpenAI API Errors
- Verify `OPENAI_API_KEY` in `.env`
- Check account has credits

### No Search Results
- Run the indexing script: `python scripts/index_docs.py --docs-dir ../book/docs`
- Verify Qdrant collection has data

## Quick Commands

```bash
# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn src.main:app --reload

# Run indexing
python scripts/index_docs.py --docs-dir ../book/docs

# Test health
curl http://localhost:8000/api/health
```

## Production Deployment

See `README.md` for production deployment instructions (Railway/Render).
