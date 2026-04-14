# AI Ad Factory

An autonomous AI-powered ad generation pipeline that creates complete advertising campaigns from a single brief. Built with 6 specialized AI agents, a full-stack web interface, and production-grade infrastructure.

## Demo

[![Watch Demo](https://img.shields.io/badge/Watch%20Demo-Loom-purple?style=for-the-badge&logo=loom)](https://www.loom.com/share/f80b83a6ec86464cb0416a8e238b4a64)

## How It Works

```
User Input (product, audience, platform, goal)
    |
    v
Optimizer Agent -----> Analyzes past top-scoring ads for patterns
    |
    v
Strategist Agent ----> Creates hook, angle, positioning (structured JSON)
    |
    v
Copywriter Agent ----> Writes ad script + call-to-action
    |
    v
Creative Director ---> Breaks script into visual scenes + shot list
    |
    v
QA Evaluator --------> Scores ad 1-10 with actionable feedback
    |
    v
Media Generator -----> Creates AI image generation prompts
    |
    v
Supabase ------------> Saves everything to PostgreSQL
    |
    v
Dashboard -----------> Displays results, history, analytics
```

## Features

- **6 AI Agents** — Each with a defined role, structured I/O, and specialized prompts
- **Self-Improving** — Optimizer agent learns from your highest-scoring ads and feeds insights into future generations
- **Background Processing** — Async job execution with real-time progress polling (not blocking for 30+ seconds)
- **Analytics Dashboard** — Score distribution charts, platform breakdown, top-performing hooks, AI-generated insights
- **Searchable History** — Browse all past ads, filter by product, one-click reuse
- **Authentication** — Email/password login via Supabase Auth with JWT validation
- **Rate Limiting** — Per-IP limits on all endpoints to prevent abuse
- **Input Validation** — Max field lengths enforced via Pydantic
- **Docker Ready** — One command to run the entire stack

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI / LLM | Claude API (Anthropic), claude-sonnet-4 |
| Backend | Python, FastAPI, Pydantic |
| Frontend | TypeScript, Next.js (App Router), Tailwind CSS |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth (JWT) |
| Charts | Recharts |
| Security | slowapi (rate limiting), input validation |
| DevOps | Docker, docker-compose |

## Quick Start

### Option 1: Local Development

**Backend:**
```bash
python -m venv venv
source venv/Scripts/activate    # Windows
pip install -r requirements.txt
uvicorn api:app --reload
```

**Frontend:**
```bash
cd ai-frontend
npm install
npm run dev
```

Open http://localhost:3000

### Option 2: Docker

```bash
docker-compose up --build
```

Open http://localhost:3000

### Environment Variables

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

## API Endpoints

| Method | Endpoint | Rate Limit | Description |
|--------|----------|-----------|-------------|
| POST | `/generate-ad` | 5/min | Start ad generation (returns job_id) |
| GET | `/jobs/{job_id}` | 60/min | Poll job status and progress |
| GET | `/ads` | 30/min | List all ads (supports `?search=`) |
| GET | `/ads/{ad_id}` | 30/min | Get single ad by ID |
| GET | `/analytics/summary` | 15/min | Dashboard statistics |
| GET | `/analytics/insights` | 5/min | AI-generated performance insights |

## Project Structure

```
ai-ad-factory/
|-- agents/                    # AI agents
|   |-- strategist.py          # Marketing strategy (JSON output)
|   |-- copywriter.py          # Ad script + CTA
|   |-- creative.py            # Visual scene breakdown
|   |-- qa.py                  # Quality scoring (1-10)
|   |-- media.py               # Image generation prompts
|   |-- optimizer.py           # Learns from past ad performance
|
|-- core/                      # Core utilities
|   |-- llm.py                 # Claude API wrapper
|   |-- db.py                  # Supabase client
|   |-- job_store.py           # Background job tracking
|   |-- analytics.py           # Analytics queries
|   |-- auth.py                # JWT auth middleware
|
|-- workflows/
|   |-- ad_pipeline.py         # 7-step pipeline orchestration
|
|-- ai-frontend/               # Next.js frontend
|   |-- app/page.tsx           # Ad generator with live progress
|   |-- app/history/page.tsx   # Searchable ad history
|   |-- app/analytics/page.tsx # Dashboard with charts
|   |-- app/login/page.tsx     # Authentication
|
|-- api.py                     # FastAPI server
|-- docker-compose.yml         # One-command deployment
|-- Dockerfile                 # Backend container
```

## Architecture Decisions

- **FastAPI BackgroundTasks over Celery** — Same async pattern without Redis infrastructure overhead. Swappable to Celery for distributed workers at scale.
- **In-memory job store** — Sufficient for single-server demo. Abstracted behind a class interface for easy swap to Redis.
- **Claude Sonnet 4** — Best balance of quality and cost for creative writing tasks.
- **Supabase** — PostgreSQL + Auth + Realtime in one service. No separate auth server needed.
- **Rate limiting with slowapi** — Prevents API abuse and Anthropic credit burning.

## Roadmap

- [ ] AI image generation (Flux via Replicate) — turn media prompts into actual images
- [ ] Ad template library — reusable layouts for common ad formats
- [ ] A/B variant generation — produce multiple ad versions from one brief
- [ ] Export to platform — direct publish to Meta, TikTok, Google Ads
