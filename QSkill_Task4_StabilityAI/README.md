# QSkill Slab 2 – Task 4: Speech-to-Image Generation

**Voice2Vision AI** converts spoken ideas into generated images using speech recognition and the Stability AI Stable Image Core API.

## Features
- Record audio in the Streamlit browser interface.
- Select a speech-recognition language (English, Hindi, Kannada, Tamil, Telugu, Malayalam, Bengali, Marathi, Spanish or French/German).
- Convert speech to editable text.
- Type a prompt manually if preferred.
- Generate an image with Stability AI Stable Image Core.
- Choose square, portrait, landscape or wide aspect ratio.
- Preview and download the generated PNG.

## Requirements
- Python 3.10+
- Internet connection
- Stability AI API key and available API credits
- Browser microphone permission

## Setup (Windows)
Open PowerShell or the VS Code terminal in the extracted project folder:

```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create your local environment file:

```powershell
copy .env.example .env
```

Open `.env` and add your real key:

```text
STABILITY_API_KEY=your_actual_stability_ai_api_key
```

Do not share your API key or commit `.env` to GitHub.

## Run
```powershell
streamlit run app.py
```

Open the local URL shown in the terminal and allow microphone access.

## Usage
1. Select the language you will speak.
2. Record your idea with the audio control.
3. Click **Convert speech to text**.
4. Review and edit the recognized prompt.
5. Select an aspect ratio and optionally enter a negative prompt.
6. Click **Generate image with Stability AI**.
7. Preview and download the resulting PNG.

## Architecture
```text
Browser microphone / typed prompt
              |
              v
        Streamlit interface
              |
       Recorded audio bytes
              |
              v
 Google speech recognition
       (selected locale)
              |
       Recognized text
              |
              v
    Stability AI REST API
     Stable Image Core
              |
       Generated PNG bytes
              |
              v
       Preview / download
```

## API integration
This project uses the Stability AI Stable Image Core endpoint:

`POST https://api.stability.ai/v2beta/stable-image/generate/core`

The endpoint returns image data directly. Unlike the original MonsterAPI design, this implementation does not create a process ID or poll a task-status endpoint.

## Troubleshooting
- **401/403:** Check that the API key is correct, active and authorized.
- **402/payment or credits error:** Check account billing and available API credits.
- **400:** Review the prompt and request parameters.
- **429:** Rate limit; wait before retrying.
- **Microphone unavailable:** Allow microphone access in browser settings or type the prompt manually.
- **Speech not recognized:** Speak clearly, choose the correct language and record again.

## Privacy and limitations
- Speech recognition sends recorded audio to Google's online recognition service.
- Image generation sends the text prompt to Stability AI.
- API usage may incur charges or consume credits. Check the current plan before generating.
- Speech-language support depends on Google's recognition service and the selected locale.
- Do not commit `.env` or expose your API key.

## Project structure
```text
QSkill_Task4_StabilityAI/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── src/
    ├── __init__.py
    ├── config.py
    ├── speech.py
    ├── stability_client.py
    └── monster_client.py  # compatibility wrapper
```
