# RAG Chatbot Testing Checklist

Complete testing guide for the RAG chatbot system.

## ✅ Setup Status

- ✅ `requirements.txt` created
- ✅ `.env` configured with all credentials
- ✅ OpenAI API key: Configured
- ✅ Qdrant Cloud: Configured (URL + API key)
- ✅ Neon Postgres: Configured (connection string)

## 🔄 Next Steps (Manual)

### Step 1: Install System Dependencies

**Run this in your terminal:**
```bash
sudo apt update && sudo apt install -y python3.12-venv python3-pip
```

### Step 2: Create Virtual Environment

```bash
cd /mnt/e/giaic/learning/spec_kit_plus/ai-native-book/backend
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 openai-1.3.5 ...
```

### Step 4: Apply Database Schema

**Connect to Neon Postgres:**
```bash
psql "postgresql://neondb_owner:npg_8XGdMNcBk2oa@ep-odd-leaf-ahcmbb1n-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
```

**Then run the schema file:**
```sql
\i ../specs/011-rag-chatbot-integration/contracts/database-schema.sql
```

**Or in one command:**
```bash
psql "postgresql://neondb_owner:npg_8XGdMNcBk2oa@ep-odd-leaf-ahcmbb1n-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require" < ../specs/011-rag-chatbot-integration/contracts/database-schema.sql
```

**Verify tables were created:**
```sql
\dt
```

Expected tables:
- `chat_sessions`
- `chat_messages`

### Step 5: Index Documentation

```bash
python scripts/index_docs.py --docs-dir ../book/docs
```

**Expected output:**
```
INFO - Starting documentation indexing...
INFO - Found 50+ markdown files
INFO - Processing intro/physical-ai.md: 3 chunks
INFO - Indexed intro/physical-ai.md (3 chunks)
...
INFO - Indexing complete: 50 files, 150+ chunks
INFO - Collection stats: {'name': 'ai_native_book', 'points_count': 150, ...}
```

**Troubleshooting:**
- If you see "Qdrant connection failed", check `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- If you see "OpenAI API error", verify `OPENAI_API_KEY` in `.env`

### Step 6: Start Backend Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Starting RAG chatbot backend...
INFO:     Database initialized
INFO:     Vector store initialized
INFO:     Backend startup complete
INFO:     Application startup complete.
```

**Keep this terminal open!**

### Step 7: Test Backend (New Terminal)

Open a new terminal and test:

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "services": {
    "qdrant": "up",
    "postgres": "up",
    "openai": "up"
  }
}
```

**Chat Query:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?"}'
```

**Expected response:**
```json
{
  "session_id": "uuid-here",
  "message": "Physical AI refers to artificial intelligence systems that interact with and manipulate the physical world...",
  "sources": [
    {
      "title": "Introduction to Physical AI",
      "file_path": "intro/physical-ai.md",
      "relevance_score": 0.92,
      "excerpt": "Physical AI is..."
    },
    ...
  ],
  "timestamp": "2025-12-01T..."
}
```

### Step 8: Start Frontend

In a new terminal:

```bash
cd /mnt/e/giaic/learning/spec_kit_plus/ai-native-book/book
npm install  # If not already installed
npm run start
```

**Expected output:**
```
Starting the development server...
Docusaurus website is running at: http://localhost:3000/
```

### Step 9: Test Chatbot UI

1. **Open browser:** http://localhost:3000
2. **Click chat button:** Bottom-right corner (💬 icon)
3. **Send test message:** "What is Physical AI?"
4. **Verify response:**
   - Response appears within 3 seconds
   - Contains 3+ source citations
   - Citations are clickable links
   - Sources show relevance scores

**Additional test queries:**
- "What is ROS2?"
- "Explain humanoid robotics"
- "What are the main components of Physical AI?"

### Step 10: Test Advanced Features

**Test 1: Conversation Context**
1. Ask: "What is Physical AI?"
2. Then ask: "What are its main components?"
3. Verify: Second response understands "its" refers to Physical AI

**Test 2: Text Selection**
1. Select text on any documentation page (10-100 characters)
2. Yellow banner should appear: "📝 Using selected text..."
3. Ask a question about the selected text
4. Verify: Response references the selected text

**Test 3: Mobile Responsive**
1. Resize browser to mobile size (≤767px)
2. Verify: Chat window goes full-screen
3. Verify: Touch targets are appropriately sized

**Test 4: Dark Mode**
1. Toggle dark mode in Docusaurus
2. Verify: Chat widget colors adapt to dark theme

**Test 5: Session Persistence**
1. Ask a question and get a response
2. Refresh the page
3. Click chat button
4. Verify: Previous conversation is still visible

**Test 6: Error Handling**
1. Stop the backend server (Ctrl+C)
2. Try sending a message
3. Verify: Error message appears with retry button
4. Restart backend and click retry
5. Verify: Message sends successfully

**Test 7: Out-of-Scope Query**
1. Ask: "What is the weather today?"
2. Verify: Response states it can only answer about book content

## 🐛 Troubleshooting

### Backend won't start
- **Error: ModuleNotFoundError**
  - Solution: Activate virtual environment: `source venv/bin/activate`
  - Solution: Install dependencies: `pip install -r requirements.txt`

- **Error: Qdrant connection failed**
  - Solution: Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
  - Solution: Check Qdrant Cloud dashboard for cluster status

- **Error: Postgres connection failed**
  - Solution: Verify `DATABASE_URL` in `.env`
  - Solution: Ensure database schema is applied
  - Solution: Check Neon dashboard for database status

- **Error: OpenAI API error**
  - Solution: Verify `OPENAI_API_KEY` in `.env`
  - Solution: Check OpenAI dashboard for account credits

### No search results
- **Symptom**: Chatbot says "I don't have information about that"
  - Solution: Run indexing script: `python scripts/index_docs.py --docs-dir ../book/docs`
  - Solution: Verify Qdrant collection has data

### Chat button not appearing
- **Symptom**: No chat button on frontend
  - Solution: Clear browser cache and reload
  - Solution: Check browser console for errors
  - Solution: Verify frontend compiled successfully

### Sources not clickable
- **Symptom**: Source citations don't link to pages
  - Solution: Verify file paths in Qdrant match documentation structure
  - Solution: Check browser console for 404 errors

## ✅ Success Criteria

All tests should pass:
- ✅ Backend health check returns "healthy"
- ✅ Chat endpoint returns responses with sources
- ✅ Frontend chat button appears on all pages
- ✅ Messages send and receive successfully
- ✅ Source citations are displayed and clickable
- ✅ Conversation context works (follow-up questions)
- ✅ Session persists across page reloads
- ✅ Mobile responsive design works
- ✅ Dark mode styling is correct
- ✅ Text selection feature works
- ✅ Error messages display on failures
- ✅ Out-of-scope queries are handled gracefully

## 📊 Performance Benchmarks

Target metrics:
- **Response time**: <3 seconds for 95% of queries
- **Source citations**: 3-5 per response
- **Relevance scores**: >0.7 for all returned chunks
- **Uptime**: Backend should start successfully

## 🎯 Next Steps After Testing

If all tests pass:
1. ✅ Mark implementation as validated
2. Update tasks.md with test results
3. Consider deploying to production (Railway/Render)
4. Implement Phase 8 polish (optional):
   - Unit tests
   - Accessibility improvements
   - Performance optimization

## 📝 Test Results Template

```
## Test Results - [Date]

### Backend Tests
- [ ] Health check: PASS/FAIL
- [ ] Chat endpoint: PASS/FAIL
- [ ] Session history: PASS/FAIL
- [ ] Error handling: PASS/FAIL

### Frontend Tests
- [ ] Chat button visible: PASS/FAIL
- [ ] Messages send/receive: PASS/FAIL
- [ ] Source citations: PASS/FAIL
- [ ] Session persistence: PASS/FAIL
- [ ] Mobile responsive: PASS/FAIL
- [ ] Dark mode: PASS/FAIL
- [ ] Text selection: PASS/FAIL

### Integration Tests
- [ ] Conversation context: PASS/FAIL
- [ ] Out-of-scope queries: PASS/FAIL
- [ ] Performance (<3s): PASS/FAIL

### Notes
[Add any issues or observations here]
```
