# Backward-compatible module name retained so app.py does not need major changes.
# Image generation is now handled by the Stability AI API.
from src.stability_client import generate_image, get_task_status, wait_for_image
