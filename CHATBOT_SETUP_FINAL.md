# RAG Chatbot Final Setup Guide

## 🎉 Current Status

### ✅ Completed:
- [x] Backend code complete and tested locally
- [x] Frontend integration complete
- [x] Documentation indexed (30 files, 66 chunks)
- [x] PR #12 merged to main
- [x] Security fixes applied (credentials removed)
- [x] Debug endpoints added for troubleshooting

### ⚠️ Pending:
- [ ] Railway deployment from main branch
- [ ] Final end-to-end testing
- [ ] GitHub Pages deployment with chatbot

---

## 🔍 **Local Testing Proves Everything Works!**

The chatbot works perfectly locally. Here's proof:

```bash
# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?"}'

# Response (summarized):
{
  "session_id": "b3b6d7b5-2fa9-47f4-aad0-0a1f31d64af3",
  "message": "Physical AI, also known as Embodied AI, represents...",
  "sources": [
    {
      "title": "Introduction to Physical AI",
      "file_path": "physical-ai/introduction.mdx",
      "relevance_score": 0.74,
      "excerpt": "Foundations of Physical AI..."
    },
    // ... 2 more sources
  ]
}
```

**All components verified working:**
- ✅ OpenAI embeddings (1536 dimensions)
- ✅ Qdrant vector search (retrieving relevant chunks)
- ✅ Neon Postgres (session management)
- ✅ GPT-4o-mini (response generation)

---

## 🚀 **Next Steps: Deploy to Production**

### Step 1: Trigger Railway Deployment

Railway should auto-deploy from `main`, but if it hasn't:

1. **Go to Railway Dashboard:**
   - https://railway.app
   - Select your project: `chatapi-production-ea84`

2. **Check Deployment Status:**
   - Click on your service
   - Check "Deployments" tab
   - Latest commit should be: `"debug: add diagnostic endpoints..."`

3. **If not deployed, manually trigger:**
   - Click "Deploy" button
   - Or go to Settings → "Redeploy"

4. **Check Deployment Logs:**
   - Look for startup message: "Backend startup complete"
   - Check for any errors

### Step 2: Verify Railway Backend

Once deployed, test these endpoints:

```bash
# 1. Health check (should work)
curl https://chatapi-production-ea84.up.railway.app/api/health

# Expected:
# {"status":"healthy","services":{"qdrant":"up","postgres":"up","openai":"up"}}

# 2. Debug components (NEW - helps identify issues)
curl https://chatapi-production-ea84.up.railway.app/api/debug/components

# Expected: All tests should show "status": "ok"

# 3. Chat endpoint (the real test)
curl -X POST https://chatapi-production-ea84.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?"}'

# Expected: JSON with message and 3 sources
```

### Step 3: Test Frontend on GitHub Pages

Your GitHub Actions should automatically deploy the frontend.

1. **Wait for GitHub Actions to complete:**
   - Go to: https://github.com/bilalmk/ai-native-book/actions
   - Check latest workflow run
   - Should deploy to: https://bilalmk.github.io/ai-native-book

2. **Test the chatbot:**
   - Visit: https://bilalmk.github.io/ai-native-book
   - Click the chat button (💬) in the bottom-right corner
   - Type: "What is Physical AI?"
   - You should get an AI response with 3 source citations

---

## 🐛 **Troubleshooting**

### Issue 1: Railway Deployment Failing

**Check Railway logs:**
```bash
railway logs --tail 100
```

**Common issues:**
- Missing environment variables
- Build failure
- Startup error

**Solution:**
Verify all environment variables in Railway dashboard:
- `OPENAI_API_KEY` ✓
- `QDRANT_URL` ✓
- `QDRANT_API_KEY` ✓
- `DATABASE_URL` ✓
- `QDRANT_COLLECTION_NAME=ai_native_book` ← **CRITICAL!**
- `CORS_ORIGINS=https://bilalmk.github.io`

### Issue 2: Chat Endpoint Returns Error

**Use debug endpoint:**
```bash
curl https://chatapi-production-ea84.up.railway.app/api/debug/components
```

**Check which component is failing:**
- `embedding`: OpenAI API key invalid
- `vector_store_search`: Collection name mismatch or empty
- `database`: Postgres connection failed

**Solutions:**
- **Embedding fails:** Check OpenAI API key, verify it has credits
- **Vector store fails:** Verify `QDRANT_COLLECTION_NAME=ai_native_book`
- **Database fails:** Check DATABASE_URL format and permissions

### Issue 3: No Search Results

**Symptom:** Chat works but always says "I don't have information"

**Cause:** Vector store is empty

**Solution:** Re-run indexing locally (it uses same Qdrant):
```bash
cd backend
source venv/bin/activate
python scripts/index_docs.py --docs-dir ../book/docs
```

### Issue 4: CORS Errors in Browser

**Symptom:** Console shows: `blocked by CORS policy`

**Solution:** Update Railway environment variable:
```bash
railway variables set CORS_ORIGINS="https://bilalmk.github.io"
```

Then redeploy Railway.

---

## 📊 **System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│               GitHub Pages (Frontend)                        │
│  https://bilalmk.github.io/ai-native-book                   │
│  - React ChatWidget                                          │
│  - Static HTML/CSS/JS                                        │
│  - Auto-deploys from main via GitHub Actions                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTPS API calls
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│            Railway (Backend)                                 │
│  https://chatapi-production-ea84.up.railway.app             │
│  - FastAPI + RAG Pipeline                                    │
│  - Auto-deploys from main branch                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ├──────► OpenAI (Embeddings + Chat)
                     ├──────► Qdrant Cloud (Vector Search)
                     └──────► Neon Postgres (Sessions)
```

---

## ✅ **Final Checklist**

Before considering this complete:

- [ ] Railway shows latest deployment (check dashboard)
- [ ] Health endpoint returns all services "up"
- [ ] Debug endpoint shows all tests passing
- [ ] Chat endpoint returns AI response with sources
- [ ] GitHub Pages deployed successfully
- [ ] Chatbot widget appears on documentation site
- [ ] Can ask questions and get responses with citations
- [ ] No CORS errors in browser console

---

## 🎯 **Quick Test Commands**

Save these for testing:

```bash
# Test Railway health
curl https://chatapi-production-ea84.up.railway.app/api/health

# Test Railway debug
curl https://chatapi-production-ea84.up.railway.app/api/debug/components | json_pp

# Test Railway chat
curl -X POST https://chatapi-production-ea84.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?"}' | json_pp

# Check Railway deployment
railway logs --tail 50

# Re-index if needed
cd backend && source venv/bin/activate && \
python scripts/index_docs.py --docs-dir ../book/docs
```

---

## 📈 **Performance & Cost**

### Expected Performance:
- **Query latency:** 2-4 seconds (embedding + search + LLM)
- **Concurrent users:** 10-20 (Railway free tier)
- **Accuracy:** High (RAG retrieves from your docs)

### Cost Estimate:
- **Railway:** Free tier (500 hrs/month)
- **GitHub Pages:** Free
- **Qdrant Cloud:** Free tier (1GB)
- **Neon Postgres:** Free tier (0.5GB)
- **OpenAI API:** ~$0.01 per query (~$5-10/month for 500-1000 queries)

**Total:** ~$5-10/month

---

## 🎉 **Success Criteria**

You'll know it's working when:

1. Visit https://bilalmk.github.io/ai-native-book
2. See chat button in bottom-right corner
3. Click it, type "What is Physical AI?"
4. Get an AI-generated answer
5. See 3 source citations with clickable links

---

## 📞 **Getting Help**

If issues persist:

1. **Check Railway logs:**
   - Most errors will appear here
   - Look for startup errors or API failures

2. **Use debug endpoint:**
   - Shows exactly which component is failing

3. **Test locally:**
   - If it works locally but not on Railway, it's a deployment/config issue
   - If it doesn't work locally, it's a code issue

4. **Common fixes:**
   - 90% of issues are missing/incorrect environment variables
   - Check `QDRANT_COLLECTION_NAME=ai_native_book` specifically
   - Verify all API keys are valid and have credits

---

## 🚀 **You're Almost There!**

Everything is coded and tested. The only thing left is ensuring Railway deploys the latest code and has the correct environment variables.

**Next Action:** Go to Railway dashboard and check deployment status.
