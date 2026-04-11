# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

Activate the virtual environment and set your API key before running anything:

```bash
source venv/Scripts/activate   # Windows Git Bash / bash
# or: venv\Scripts\activate.bat  (cmd) / venv\Scripts\Activate.ps1 (PowerShell)
```

Copy `.env` and fill in your key:
```
ANTHROPIC_API_KEY=sk-ant-...
```

The project uses `python-dotenv`, so `.env` is loaded automatically when the module calls `load_dotenv()`.

## Installed dependencies

The venv already has these packages pinned:
- `anthropic` — Anthropic Python SDK (Claude API)
- `python-dotenv` — `.env` loading
- `pydantic` — data validation / typed models
- `httpx` / `httpcore` — async HTTP (used internally by the Anthropic SDK)

No `requirements.txt` exists yet; install new packages into the venv and document them here or in a requirements file.

## Architecture

The project is an AI-powered advertising strategy generator. The intended data flow:

```
Input: product, audience, platform, goal
    → agents/strategist.py   (orchestrates the request)
    → core/llm.py            (wraps Anthropic SDK calls)
    → prompts/               (stores prompt templates)
    → workflows/             (multi-step orchestration, if needed)
Output: hook, angle, positioning
```

**agents/strategist.py** — the main agent; currently holds the input/output specification as a comment stub. This is where the top-level logic (prompt construction, response parsing) should live.

**core/llm.py** — the LLM integration layer. Should encapsulate the `anthropic.Anthropic` client, handle API calls, and expose a clean interface so agents aren't coupled to the SDK directly.

**prompts/** — intended for prompt template files (e.g., Jinja2 or plain `.txt`/`.md` templates).

**workflows/** — intended for multi-step or chained agent workflows.

## Running the project

No entry point script exists yet. Once implemented, the expected invocation will be something like:

```bash
python agents/strategist.py
```
