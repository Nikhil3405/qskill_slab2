import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(page_title="MemoryAI Chat", page_icon="✦", layout="wide")

SYSTEM_INSTRUCTION = """You are MemoryAI, a helpful and accurate assistant.
Use the conversation history provided below to understand follow-up questions.
If Google Search grounding is enabled for this request, use current search information
when useful and clearly distinguish sourced facts from uncertainty.
If the user asks what was said earlier, use the supplied conversation history.
If the history does not contain the requested detail, say so rather than inventing it.
Keep answers clear, structured, and useful."""

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
MAX_HISTORY_MESSAGES = 12

def get_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def build_prompt(history, current_message):
    recent = history[-MAX_HISTORY_MESSAGES:]
    transcript = []
    for item in recent:
        role = "User" if item["role"] == "user" else "Assistant"
        transcript.append(f"{role}: {item['content']}")
    history_text = "\n".join(transcript) if transcript else "(No earlier messages.)"
    return (
        f"{SYSTEM_INSTRUCTION}\n\n"
        f"Conversation history:\n{history_text}\n\n"
        f"Current user message:\nUser: {current_message}\n\n"
        "Assistant:"
    )

def extract_citations(response):
    citations = []
    try:
        candidates = getattr(response, "candidates", []) or []
        for candidate in candidates:
            metadata = getattr(candidate, "grounding_metadata", None)
            chunks = getattr(metadata, "grounding_chunks", []) or []
            for chunk in chunks:
                web_item = getattr(chunk, "web", None)
                if web_item is None:
                    continue
                url = getattr(web_item, "uri", None)
                title = getattr(web_item, "title", None) or "Source"
                if url and all(source["url"] != url for source in citations):
                    citations.append({"title": title, "url": url})
    except Exception:
        # The answer can still be shown if citation metadata differs by SDK version.
        pass
    return citations

def ask_gemini(client, history, message, use_search):
    prompt = build_prompt(history, message)
    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())] if use_search else None
    )
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )
    answer = getattr(response, "text", None)
    if not answer:
        answer = "I couldn't generate a text response. Please try again."
    return answer, extract_citations(response)

# Sidebar
with st.sidebar:
    st.markdown("## ✦ MemoryAI")
    st.caption("A conversational assistant with session memory and Google Search.")
    st.markdown("---")
    st.markdown("### Settings")
    use_search = st.toggle("Enable Google Search", value=False,
                           help="Allows Gemini to search the web for current information. Search usage may be billable.")
    st.caption(f"Model: `{MODEL_NAME}`")
    st.markdown("---")
    if st.button("＋ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("**Memory status**")
    count = len(st.session_state.get("messages", []))
    st.write(f"{count} messages in this browser session")
    st.caption("Memory is temporary and resets when you start a new conversation or the session is cleared.")

st.title("✦ MemoryAI")
st.write("Ask a question, continue a previous topic, or enable Google Search for current information.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous messages and their sources
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for source in msg["sources"]:
                    st.markdown(f"- [{source['title']}]({source['url']})")

api_key_present = bool(os.getenv("GEMINI_API_KEY", "").strip())
if not api_key_present:
    st.warning("Gemini API key not found. Add GEMINI_API_KEY to your .env file, then restart Streamlit.")

prompt = st.chat_input("Message MemoryAI...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key_present:
        error_text = "Please configure GEMINI_API_KEY in your .env file and restart the application."
        st.session_state.messages.append({"role": "assistant", "content": error_text, "sources": []})
        with st.chat_message("assistant"):
            st.error(error_text)
    else:
        try:
            client = get_client()
            # Exclude the current user message from history because it is passed separately.
            prior_history = st.session_state.messages[:-1]
            with st.chat_message("assistant"):
                with st.spinner("Thinking..." if not use_search else "Thinking and searching the web..."):
                    answer, sources = ask_gemini(client, prior_history, prompt, use_search)
                st.markdown(answer)
                if sources:
                    with st.expander("Sources"):
                        for source in sources:
                            st.markdown(f"- [{source['title']}]({source['url']})")
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
        except Exception as exc:
            error_text = (
                f"Gemini request failed: {exc}\n\n"
                "Check your API key, model availability, internet connection and API quota."
            )
            with st.chat_message("assistant"):
                st.error(error_text)
            st.session_state.messages.append({"role": "assistant", "content": error_text, "sources": []})

st.markdown("---")
st.caption("MemoryAI is an educational demo. Conversation memory is held in Streamlit session state and is not saved to a permanent database.")
