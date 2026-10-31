class SpeechIO:
    def __init__(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 175)
        except Exception:
            self.engine = None

    def speak(self, text):
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass

    def listen(self):
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            return recognizer.recognize_google(audio)
        except ImportError:
            print("SpeechRecognition is missing; use typed commands.")
        except Exception as exc:
            print(f"Voice input unavailable ({exc}); use typed commands.")
        return None
