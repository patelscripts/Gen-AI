# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A **learning / playground** repo for Gen-AI experiments using the LangChain ecosystem. Currently contains two topic folders — `chatmodels/` and `embeddings/` — used to try out different providers and patterns. See `README.md`: *"this is basically for learning purpose."*

There is no production architecture here; each subfolder is an independent scratchpad. Keep new explorations self-contained (one folder per experiment) rather than wiring them into shared modules.

## Environment

- **Python:** `3.14` (pinned in `.python-version` and `pyproject.toml`'s `requires-python`). The interpreter in use is the system Python 3.14.
- **Package manager:** `uv` (a `uv.lock` and a `.venv/` directory are present). Prefer `uv` over `pip` for installs and runs.
- **OS / shell:** Windows, PowerShell primary.
- **API keys:** stored in `.env` at the repo root and loaded via `python-dotenv`'s `load_dotenv()`. Keys present: `GROQ_API_KEY`, `GOOGLE_API_KEY`, `MISTRAL_API_KEY`. The `.env` file is gitignored.

## Common Commands

Use the project's venv python (referenced from `.claude/settings.local.json`):

```powershell
# Run a script using the existing venv
& "d:\gen AI\.venv\Scripts\python.exe" "d:/gen AI/chatmodels/chat.py"

# Or from the repo root with uv
uv run python chatmodels/chat.py

# Install / sync dependencies
uv sync
pip install -r requirements.txt      # fallback

# Add a new dependency (and the wider ecosystem listed in requirements.txt)
uv add <package>
```

## Repository Structure

```
gen-ai/
├── chatmodels/        # chat model experiments (provider × prompt × pattern)
│   └── chat.py        # minimal Gemini Flash example using init_chat_model
├── embeddings/        # empty — reserved for embedding experiments
├── main.py            # boilerplate entry point ("Hello from gen-ai!")
├── pyproject.toml     # pins langchain-google-genai>=4.3.2, python>=3.14
├── requirements.txt   # full dep list: langchain, langchain-{groq,google-genai,mistralai}, pydantic, fastapi, uvicorn, python-dotenv
├── .env               # NOT committed — API keys live here
└── .venv/             # local virtualenv
```

## Key Patterns Established

The canonical pattern used in `chatmodels/chat.py` is the one to imitate when adding new model experiments:

1. Group all `import` statements at the top (`os`, third-party).
2. Call `load_dotenv()` once, immediately after imports.
3. **Fail fast** if the required provider key is missing — `if not os.getenv("KEY"): raise RuntimeError(...)` — instead of letting the API surface a cryptic auth error.
4. Build the model with `langchain.chat_models.init_chat_model("<model-id>", model_provider="<provider>")`.
5. Call `model.invoke("<prompt>")` (sync) and print `response.content`.

Provider-specific `model_provider` strings used in this repo: `google_genai` (Gemini), and equivalents for Groq / Mistral when those folders are populated.

## Known Gotchas

- **`uuid_utils` DLL block on Windows**: with Python 3.14 the Rust-compiled `uuid_utils` extension required by `langchain_core` is sometimes blocked by Windows Application Control, surfacing as `ImportError: DLL load failed while importing _uuid_utils: An Application Control policy has blocked this file.` Fixes: (1) add a Defender exclusion / `Unblock-File` on `D:\gen AI\.venv\Lib\site-packages\uuid_utils\`, or (2) recreate the venv on Python 3.11/3.12, or (3) `pip uninstall uuid_utils -y && pip install uuid_utils`.
- **LangChain import path**: on `langchain>=0.3`, `init_chat_model` moved from `langchain.chat_models` to top-level `langchain`. The current files use the old path; if you see `ImportError`, switch to `from langchain import init_chat_model` (or guard with a `try/except ImportError` shim).
- **API-key format sanity-check**: Google's keys start with `AIza`; an unrelated-looking value in `.env` will fail auth even when the call site is correct. Verify with `print(os.getenv("GOOGLE_API_KEY", "")[:6])` after `load_dotenv()` before debugging deeper.
- **`.env` is gitignored** — never commit it. If a teammate needs keys, copy from `.env.example` (not yet present; create one when adding new keys).

## When Adding a New Experiment

1. Create a folder under the repo root named after the topic (`chatmodels/`, `embeddings/`, `agents/`, …).
2. Add a single `*.py` file inside that folder using the four-step pattern above.
3. Don't import across experiment folders — each should run standalone with `python <folder>/<file>.py`.
4. If new dependencies are needed, prefer declaring them in `pyproject.toml` (the source of truth) and mirroring in `requirements.txt`, then `uv sync`.
