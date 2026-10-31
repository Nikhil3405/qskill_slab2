# MemoryAI — Gemini Conversational Memory with Google Search

A Python chatbot application built with Streamlit and Google's Gemini API. It maintains recent conversation history during the active Streamlit session and can optionally use Gemini's built-in Google Search grounding for current information.

## Features
- Chat interface with user and assistant message history.
- Context-aware follow-up questions using recent conversation turns.
- Optional Google Search grounding toggle.
- Displays source links returned as grounding citations when available.
- New conversation control.
- API key stored in a local `.env` file, not in source code.

## Tech stack
Python, Streamlit, Google Gen AI SDK (`google-genai`), Gemini API, Google Search grounding and python-dotenv.

## Setup

Python 3.10+ recommended.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Configure Gemini API key
1. Create or open a project in Google AI Studio and create a Gemini API key.
2. Copy `.env.example` to a new file named `.env`.
3. Put your key in `.env`:

```env
GEMINI_API_KEY=your_actual_key
GEMINI_MODEL=gemini-2.5-flash
```

Never commit `.env` or share your API key. `.gitignore` excludes it.

## Run
```bash
streamlit run app.py
```
Open the local URL printed by Streamlit, usually http://localhost:8501.

## How conversational memory works
Streamlit stores messages in `st.session_state`. Before each Gemini request, the application formats the most recent conversation messages into a prompt together with the current user message. This allows Gemini to answer follow-up questions based on earlier turns in the same active session. The app retains up to the most recent 12 history messages in each prompt to keep requests bounded.

This is session memory, not permanent user memory. Starting a new conversation clears the messages. Restarting the app or losing the session may also clear them.

## How Google Search works
When **Enable Google Search** is switched on, the app sends the request to Gemini with its built-in `google_search` tool. Gemini decides whether a search is useful, incorporates relevant results and may return URL citation annotations. The app displays available source links.

This uses Gemini's Google Search grounding feature; it does not call the legacy Custom Search JSON API directly. Google's Custom Search JSON API is closed to new customers, so Gemini's built-in grounding is the supported approach for this project.

## Test prompts
1. `My name is Alex and I am learning Python.`
2. `What am I learning?` — checks conversational context.
3. `Who is the current president of the United States?` — enable Google Search and check whether sources are displayed.
4. `Summarize what we discussed earlier.`

## Limitations
- Conversation history is temporary and session-scoped.
- The application sends recent conversation text to the Gemini API; do not enter passwords, secrets or sensitive personal information.
- Search grounding availability, model access, quotas and billing depend on the Google AI Studio project and current Google terms.
- Model answers can still be inaccurate. Check citations for time-sensitive claims.
