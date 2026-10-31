# QSkill Slab 2 – Voice-Activated Personal Assistant

A Python assistant with microphone-based speech recognition, spoken responses, reminders, current weather, news headlines, and basic desktop actions.

## Features
- Speech-to-text with SpeechRecognition and Google's online recognition service.
- Text-to-speech with pyttsx3.
- Set reminders by duration or 24-hour clock time.
- Current weather using the free Open-Meteo API (no API key).
- World headlines from BBC News RSS (no API key).
- Tell time/date; open Google and YouTube.
- Typed-command fallback if microphone input is unavailable.

## Requirements
Python 3.10+, microphone, and internet for speech recognition/weather/news.

## Install and run
```bash
python -m venv venv
```
Windows:
```bash
venv\\Scripts\\activate
```
macOS/Linux:
```bash
source venv/bin/activate
```
Then:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

### Windows PyAudio note
If `pip install PyAudio` fails, install a PyAudio wheel compatible with your Python version and Windows architecture, then run:
```bash
pip install SpeechRecognition pyttsx3
```
Typed commands still work without microphone input.

## Example commands
- `weather in Bengaluru`
- `news`
- `remind me in 10 minutes to drink water`
- `set reminder for 14:30 to call Sam`
- `what time is it`
- `what is the date`
- `open YouTube`
- `help`
- `exit`

Keep the program running until a reminder is due. Reminders are held in memory and disappear when the program exits.

## How it works
1. SpeechIO captures speech and converts it into text.
2. VoiceAssistant routes the recognized command to the matching feature.
3. Open-Meteo provides geocoding and current weather data.
4. The assistant parses BBC RSS XML to get headline titles.
5. pyttsx3 speaks the response aloud.

## Limitations and privacy
- The Google speech-recognition endpoint receives audio for transcription.
- Weather, news and speech recognition require internet access.
- This demo does not continuously listen for a wake word.
- Reminders are not saved after the app closes.
- BBC World News RSS is the configured news source.

## Project structure
```text
QSkill_Slab2_Voice_Assistant/
├── app.py
├── requirements.txt
├── README.md
└── assistant/
    ├── __init__.py
    ├── core.py
    ├── services.py
    └── speech.py
```
