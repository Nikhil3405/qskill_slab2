import base64
import requests
from src.config import get_api_key

BASE_URL = "https://api.stability.ai"

def _headers():
    key = get_api_key()
    if not key:
        raise ValueError("STABILITY_API_KEY is missing from .env.")
    return {
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
    }

def generate_image(
    prompt: str,
    negative_prompt: str = "",
    aspect_ratio: str = "1:1",
) -> bytes:
    """
    Generate an image using Stability AI's synchronous Stable Image Core endpoint.
    Returns the image bytes directly (PNG).
    """
    if not prompt or not prompt.strip():
        raise ValueError("Please provide a text prompt.")

    payload = {
        "prompt": prompt.strip(),
        "output_format": "png",
        "aspect_ratio": aspect_ratio,
    }
    if negative_prompt and negative_prompt.strip():
        payload["negative_prompt"] = negative_prompt.strip()

    response = requests.post(
        f"{BASE_URL}/v2beta/stable-image/generate/core",
        headers={**_headers(), "Accept": "image/*"},
        files={"none": ""},
        data=payload,
        timeout=180,
    )

    if not response.ok:
        try:
            details = response.json()
        except ValueError:
            details = response.text[:1500]
        raise RuntimeError(
            f"Stability AI returned HTTP {response.status_code}: {details}"
        )

    content_type = response.headers.get("Content-Type", "")
    if "image" not in content_type.lower():
        raise RuntimeError(
            f"Stability AI did not return an image. Content-Type: {content_type}. "
            f"Response: {response.text[:1000]}"
        )
    return response.content

def get_task_status(process_id: str):
    raise NotImplementedError(
        "The Stable Image Core endpoint returns the generated image directly; "
        "it does not use MonsterAPI-style process IDs or status polling."
    )

def wait_for_image(process_id: str, timeout_seconds: int = 240, poll_interval: int = 5):
    return get_task_status(process_id)
