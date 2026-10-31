import io
import speech_recognition as sr

def transcribe_audio(audio_bytes: bytes, language: str) -> str:
    """Convert recorded audio to text using Google's online speech recognition."""
    if not audio_bytes:
        raise ValueError("The audio recording is empty.")
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language=language)
        if not text.strip():
            raise ValueError("No speech was recognized. Please record again.")
        return text.strip()
    except sr.UnknownValueError as exc:
        raise ValueError("Speech could not be understood. Speak clearly and try again.") from exc
    except sr.RequestError as exc:
        raise RuntimeError(f"Speech recognition service error: {exc}") from exc
