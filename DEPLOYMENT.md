# Production Deployment Guide

This guide explains how to deploy the AI Native Book with the RAG chatbot to production.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Pages                              │
│  (Frontend: Docusaurus + React ChatWidget)                  │
│  URL: https://bilalmk.github.io/ai-native-book              │
│  - Static HTML/CSS/JS only                                   │
│  - NO credentials needed                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTPS API calls
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│            Backend Hosting Platform                          │
│  (FastAPI + RAG Service)                                    │
│  URL: https://your-backend.railway.app (or similar)         │
│  - Python runtime environment                                │
│  - Environment variables with REAL credentials              │
│  - Accesses: OpenAI, Qdrant, Neon Postgres                  │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

Before deploying, ensure you have:

1. ✅ **GitHub account** - for frontend hosting
2. ✅ **OpenAI API key** - from https://platform.openai.com/api-keys
3. ✅ **Qdrant Cloud account** - free tier at https://cloud.qdrant.io
4. ✅ **Neon Postgres database** - free tier at https://neon.tech
5. ✅ **Backend hosting account** - Railway, Render, or Vercel (see options below)

---

## Part 1: Deploy Backend (FastAPI + RAG Service)

The backend needs to be deployed to a platform that supports Python runtime and environment variables.

### Option A: Railway.app (Recommended) ⭐

**Why Railway?**
- Free tier with 500 hours/month
- Automatic HTTPS
- Easy environment variable management
- GitHub integration
- Fast deployment

**Step-by-step:**

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize project:**
   ```bash
   cd backend
   railway init
   # Follow prompts to create new project
   ```

4. **Add environment variables:**
   ```bash
   railway variables set OPENAI_API_KEY="sk-proj-your-real-key-here"
   railway variables set QDRANT_URL="https://your-cluster.cloud.qdrant.io:6333"
   railway variables set QDRANT_API_KEY="your-qdrant-key"
   railway variables set DATABASE_URL="postgresql://user:pass@host.neon.tech/db"
   railway variables set QDRANT_COLLECTION_NAME="ai_native_book"
   railway variables set ENVIRONMENT="production"
   railway variables set CORS_ORIGINS="https://bilalmk.github.io"
   ```

5. **Deploy:**
   ```bash
   railway up
   ```

6. **Get your backend URL:**
   ```bash
   railway domain
   # Output: https://your-app-name.up.railway.app
   ```

7. **Verify deployment:**
   ```bash
   curl https://your-app-name.up.railway.app/api/health
   ```

---

### Option B: Render.com

**Why Render?**
- Free tier available
- Automatic deploys from GitHub
- Built-in database options
- Good for beginners

**Step-by-step:**

1. **Go to:** https://render.com
2. **Create new Web Service**
3. **Connect your GitHub repository**
4. **Configure settings:**
   - **Name:** `ai-native-book-backend`
   - **Region:** Choose closest to your users
   - **Branch:** `main` or `011-rag-chatbot-integration`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

5. **Add environment variables** (in Render dashboard):
   ```
   OPENAI_API_KEY=sk-proj-your-real-key-here
   QDRANT_URL=https://your-cluster.cloud.qdrant.io:6333
   QDRANT_API_KEY=your-qdrant-key
   DATABASE_URL=postgresql://user:pass@host.neon.tech/db
   QDRANT_COLLECTION_NAME=ai_native_book
   ENVIRONMENT=production
   CORS_ORIGINS=https://bilalmk.github.io
   ```

6. **Deploy** - Render will automatically build and deploy

7. **Your backend URL:** `https://ai-native-book-backend.onrender.com`

---

### Option C: Vercel (Serverless)

**Why Vercel?**
- Free tier with good limits
- Automatic HTTPS and CDN
- Fast cold starts
- Easy GitHub integration

**Step-by-step:**

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Create `vercel.json` in backend directory:**
   ```json
   {
     "builds": [
       {
         "src": "src/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "src/main.py"
       }
     ]
   }
   ```

3. **Deploy:**
   ```bash
   cd backend
   vercel
   # Follow prompts
   ```

4. **Add environment variables** (in Vercel dashboard):
   - Go to your project settings
   - Add all environment variables from above

5. **Your backend URL:** `https://your-project.vercel.app`

---

## Part 2: Index Your Documentation

Before the chatbot can work, you need to populate the Qdrant vector database with your documentation.

**Run this once after deploying backend:**

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with your production credentials
cp .env.example .env
# Edit .env and add your REAL credentials

# Run indexing script
python scripts/index_docs.py --docs-dir ../book/docs

# Expected output:
# INFO - Found 50+ markdown files
# INFO - Processing file.md: 3 chunks
# ...
# INFO - Indexing complete: 50 files, 150+ chunks
```

**Verify indexing worked:**
```bash
# Test your production backend
curl -X POST https://your-backend-url.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?"}'

# Should return JSON with answer and 3+ sources
```

---

## Part 3: Configure Frontend to Use Backend

Update the frontend to point to your deployed backend.

1. **Edit the API configuration:**
   ```bash
   # File: book/src/theme/components/ChatWidget/api/chatApi.ts
   ```

2. **Replace the production URL:**
   ```typescript
   const API_BASE_URL = process.env.NODE_ENV === 'production'
     ? 'https://your-actual-backend-url.railway.app'  // ← Change this!
     : 'http://localhost:8000';
   ```

3. **Commit the change:**
   ```bash
   git add book/src/theme/components/ChatWidget/api/chatApi.ts
   git commit -m "config: update production backend URL"
   git push origin main
   ```

---

## Part 4: Deploy Frontend to GitHub Pages

Your Docusaurus site can be deployed to GitHub Pages for free static hosting.

1. **Update `docusaurus.config.js`:**
   ```bash
   # File: book/docusaurus.config.js
   ```

   Ensure these settings are correct:
   ```javascript
   module.exports = {
     url: 'https://bilalmk.github.io',
     baseUrl: '/ai-native-book/',
     organizationName: 'bilalmk',
     projectName: 'ai-native-book',
     deploymentBranch: 'gh-pages',
   };
   ```

2. **Enable GitHub Pages:**
   - Go to your repo: https://github.com/bilalmk/ai-native-book
   - Go to **Settings** → **Pages**
   - Under **Source**, select branch: `gh-pages` and folder: `/ (root)`
   - Click **Save**

3. **Deploy using GitHub Actions (recommended):**

   Create `.github/workflows/deploy.yml`:
   ```yaml
   name: Deploy to GitHub Pages

   on:
     push:
       branches:
         - main

   jobs:
     deploy:
       name: Deploy to GitHub Pages
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-node@v3
           with:
             node-version: 18
             cache: npm
             cache-dependency-path: book/package-lock.json

         - name: Install dependencies
           run: cd book && npm ci

         - name: Build website
           run: cd book && npm run build

         - name: Deploy to GitHub Pages
           uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./book/build
   ```

4. **Or deploy manually:**
   ```bash
   cd book
   npm install
   npm run build

   # Deploy (requires Git and SSH configured)
   GIT_USER=bilalmk npm run deploy
   ```

5. **Verify deployment:**
   - Visit: https://bilalmk.github.io/ai-native-book
   - Click the chat button (💬) in bottom-right
   - Ask: "What is Physical AI?"
   - You should get an answer with 3+ source citations

---

## Part 5: Verify Complete System

### Test Backend Health:
```bash
curl https://your-backend-url.com/api/health

# Expected response:
# {
#   "status": "healthy",
#   "services": {
#     "qdrant": "up",
#     "postgres": "up",
#     "openai": "up"
#   }
# }
```

### Test Backend Chat:
```bash
curl -X POST https://your-backend-url.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?"}'

# Expected response:
# {
#   "session_id": "uuid-here",
#   "message": "Physical AI refers to...",
#   "sources": [
#     {
#       "title": "Introduction to Physical AI",
#       "file_path": "docs/intro.md",
#       "relevance_score": 0.85,
#       "excerpt": "..."
#     },
#     ...
#   ]
# }
```

### Test Frontend:
1. Visit: https://bilalmk.github.io/ai-native-book
2. Open browser DevTools → Console
3. Click chat button
4. Ask a question
5. Check Network tab for API calls to your backend
6. Verify no CORS errors

---

## Troubleshooting

### CORS Errors in Browser Console

**Symptom:** `Access to fetch at 'https://backend' from origin 'https://github.io' has been blocked by CORS policy`

**Solution:**
1. Verify `CORS_ORIGINS` environment variable includes your GitHub Pages URL:
   ```bash
   railway variables set CORS_ORIGINS="https://bilalmk.github.io"
   ```
2. Restart your backend service
3. Clear browser cache and try again

---

### Backend Returns 500 Error

**Symptom:** Chat widget shows "Failed to send message"

**Solution:**
1. Check backend logs:
   ```bash
   railway logs  # For Railway
   # Or check Render/Vercel dashboard
   ```
2. Common issues:
   - Missing environment variables
   - Invalid OpenAI API key
   - Qdrant collection not indexed
   - Database connection failed

---

### No Search Results Returned

**Symptom:** Backend responds but says "I don't have information about that"

**Solution:**
1. Verify Qdrant collection has data:
   ```bash
   python scripts/index_docs.py --docs-dir ../book/docs
   ```
2. Check collection name matches:
   - Environment variable: `QDRANT_COLLECTION_NAME=ai_native_book`
   - Config.py default: `documentation_chunks`
   - Make sure they match!

---

### Frontend Shows "Connecting to backend..."

**Symptom:** Chat widget stuck in loading state

**Solution:**
1. Verify backend URL in `chatApi.ts` is correct
2. Test backend health endpoint directly:
   ```bash
   curl https://your-backend-url.com/api/health
   ```
3. Check browser console for errors
4. Verify backend is running (not sleeping on free tier)

---

## Environment Variables Reference

### Backend (.env)

```bash
# OpenAI
OPENAI_API_KEY=sk-proj-your-real-key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small  # optional
OPENAI_CHAT_MODEL=gpt-4o-mini  # optional

# Qdrant
QDRANT_URL=https://your-cluster.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=ai_native_book

# Neon Postgres
DATABASE_URL=postgresql://user:pass@host.neon.tech/db?sslmode=require

# Application
ENVIRONMENT=production
CORS_ORIGINS=https://bilalmk.github.io
LOG_LEVEL=INFO  # optional
```

---

## Cost Estimation (Free Tier)

| Service | Free Tier | Typical Usage | Cost |
|---------|-----------|---------------|------|
| **Railway** | 500 hrs/month | ~20 hrs/month (sleeping enabled) | $0 |
| **Render** | 750 hrs/month | 750 hrs/month (always on) | $0 |
| **GitHub Pages** | Unlimited | Static hosting | $0 |
| **Qdrant Cloud** | 1GB storage | ~50MB for docs | $0 |
| **Neon Postgres** | 0.5GB storage | ~10MB for sessions | $0 |
| **OpenAI API** | Pay-as-you-go | ~$0.50/1000 messages | ~$5-10/month |

**Total estimated cost:** $5-10/month (mostly OpenAI usage)

---

## Security Checklist

- [ ] ✅ All API keys stored in environment variables (not in code)
- [ ] ✅ `.env` file is in `.gitignore`
- [ ] ✅ `env.example` contains only placeholder values
- [ ] ✅ CORS configured to only allow your GitHub Pages domain
- [ ] ✅ Rate limiting enabled (60 queries/hour per IP)
- [ ] ✅ Database uses SSL connections
- [ ] ✅ Backend uses HTTPS (automatic on Railway/Render/Vercel)

---

## Monitoring and Maintenance

### Check Backend Health:
```bash
# Set up a cron job or uptime monitor
curl https://your-backend-url.com/api/health
```

### Monitor OpenAI Usage:
- Dashboard: https://platform.openai.com/usage
- Set up billing alerts to avoid surprises

### Monitor Backend Logs:
```bash
railway logs  # Railway
# Or use Render/Vercel dashboard
```

### Update Documentation Index:
When you add new documentation, re-run indexing:
```bash
python scripts/index_docs.py --docs-dir ../book/docs
```

---

## Next Steps

1. ✅ Deploy backend to Railway/Render/Vercel
2. ✅ Index documentation into Qdrant
3. ✅ Update frontend API URL
4. ✅ Deploy frontend to GitHub Pages
5. ✅ Test complete system
6. 🎉 Share your AI-powered documentation with the world!

---

## Support

- **Railway:** https://railway.app/help
- **Render:** https://render.com/docs
- **Vercel:** https://vercel.com/docs
- **OpenAI:** https://help.openai.com
- **Qdrant:** https://qdrant.tech/documentation
- **Neon:** https://neon.tech/docs

---

## License

Same as the main project.
