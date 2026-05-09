# Repository Guidelines

## Project Structure & Module Organization

This repository is a small Flask application with a static frontend.

- `app.py` defines the Flask app, serves `frontend/index.html`, and exposes `POST /api/chat`.
- `llm.py` contains OpenAI client setup and streaming response logic.
- `frontend/index.html` contains the complete HTML, CSS, and browser JavaScript UI.
- `requirements.txt` lists Python runtime dependencies.
- `.env` is used for local secrets such as `OPENAI_API_KEY`; do not commit it.

Keep backend request validation and routing in `app.py`. Keep provider-specific LLM calls in `llm.py`. Add static assets under `frontend/` if the UI grows.

## Build, Test, and Development Commands

Create and activate a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Run locally:

```sh
python app.py
```

The app starts Flask in debug mode and serves the UI at `http://127.0.0.1:5000/`.

## Coding Style & Naming Conventions

Use Python 3 with 4-space indentation, clear function names, and type hints for reusable helpers, following the current `stream_llm(...) -> Iterator[str]` style. Prefer small functions and keep error messages user-facing where they cross the API boundary.

Frontend code currently uses plain HTML, CSS, and JavaScript in one file. Use `camelCase` for JavaScript variables and functions, and descriptive `id` names that match their purpose, such as `sendBtn` and `responseBox`.

## Testing Guidelines

No automated test suite is currently present. When adding tests, create a `tests/` directory and use `pytest` for backend behavior. Name files `test_*.py` and focus on Flask route validation, model allow-list behavior, and streaming error handling.

Run future tests with:

```sh
pytest
```

For frontend changes, manually verify prompt submission, empty prompt validation, model selection, and streamed output rendering in a browser.

## Commit & Pull Request Guidelines

Recent commits use short, direct messages, sometimes in Turkish, for example `Add streaming LLM responses` and `requirements.txt olusturuldu`. Keep commits concise and imperative where possible, such as `Validate chat payload`.

Pull requests should include a brief summary, testing notes, any required `.env` changes, and screenshots or screen recordings for UI changes. Link related issues when available.

## Security & Configuration Tips

Store API keys only in `.env` and load them through `python-dotenv`. Never print secrets in logs or return raw provider errors to the browser. Update `ALLOWED_MODELS` in `app.py` and the model `<select>` in `frontend/index.html` together.
