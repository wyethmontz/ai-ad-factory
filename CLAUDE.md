# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Setup

### Backend
```bash
cd ai-ad-factory
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
uvicorn api:app --reload
```

### Frontend
```bash
cd ai-frontend
npm install
npm run dev
```

### Docker (runs both)
```bash
docker-compose up --build
```

### Environment variables
Backend `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
```

Frontend `ai-frontend/.env.local`:
```
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Architecture

AI-powered ad generation pipeline with 6 agents:

```
User Input (product, audience, platform, goal)
   → Optimizer        (learns from past top-scoring ads)
   → Strategist       (creates hook, angle, positioning as JSON)
   → Copywriter       (writes ad script + CTA)
   → Creative Director (breaks into visual scenes)
   → QA Evaluator     (scores 1-10 with feedback)
   → Media Generator  (creates AI image prompts)
   → Supabase         (saves everything)
   → Frontend         (displays results)
```

### Backend (Python / FastAPI)
- `api.py` — FastAPI server with all routes
- `agents/` — 6 AI agents (strategist, copywriter, creative, qa, media, optimizer)
- `core/llm.py` — Claude API wrapper (claude-sonnet-4)
- `core/db.py` — Supabase client + save_ad()
- `core/job_store.py` — In-memory background job tracking
- `core/analytics.py` — Analytics queries
- `core/auth.py` — JWT auth middleware (Supabase Auth)
- `workflows/ad_pipeline.py` — 7-step pipeline orchestration

### Frontend (TypeScript / Next.js)
- `app/page.tsx` — Generate Ad page (form + polling + results)
- `app/history/page.tsx` — Searchable ad history with cards
- `app/analytics/page.tsx` — Dashboard with charts (recharts)
- `app/login/page.tsx` — Supabase Auth login/signup
- `app/components/` — Sidebar, AdCard, SearchBar, AuthGuard

### API Endpoints
- `POST /generate-ad` — Starts pipeline (returns job_id, async)
- `GET /jobs/{job_id}` — Poll job status and progress
- `GET /ads` — List ads (supports ?search= filter)
- `GET /ads/{ad_id}` — Get single ad
- `GET /analytics/summary` — Dashboard stats
- `GET /analytics/insights` — AI-generated insights

## Security Checklist

IMPORTANT: Apply these whenever adding new endpoints or deploying:

1. **Rate limiting** — Every public endpoint must have rate limits to prevent credit burning and DoS. Use `slowapi` or similar. Suggested limits:
   - `/generate-ad` → 5 requests/minute per IP
   - `/ads`, `/analytics` → 30 requests/minute per IP
   - `/login` → 10 requests/minute per IP

2. **Input validation** — All user inputs must have max length:
   - product, audience, platform, goal → max 200 characters each
   - search query → max 100 characters
   - Reject requests over 10KB total

3. **CORS** — Lock down to specific frontend origin in production. Never ship `allow_origins=["*"]` to prod.

4. **Auth on sensitive routes** — Use `core/auth.py` dependency on routes that should require login.

5. **API keys** — Never hardcode. Always use .env files. Never commit .env to git.

6. **HTTPS** — Required for any public deployment. Use a reverse proxy (nginx, Caddy) or platform TLS (Vercel, Railway).

## Database (Supabase)

Table: `ads`
Columns: id (uuid), product, audience, platform, goal, hook, angle, positioning, copy, creative, qa_score, qa_score_numeric (int), media, images (text), created_at (timestamptz)

## Dependencies

Backend: see `requirements.txt`
Frontend: see `ai-frontend/package.json`
