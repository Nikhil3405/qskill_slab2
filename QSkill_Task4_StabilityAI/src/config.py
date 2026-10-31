import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    """Return the Stability AI API key."""
    return os.getenv("STABILITY_API_KEY", "").strip()
