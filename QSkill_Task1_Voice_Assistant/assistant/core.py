import datetime as dt
import queue
import re
import threading
import time
import webbrowser
from assistant.speech import SpeechIO
from assistant.services import get_weather, get_headlines

class VoiceAssistant:
    def __init__(self):
        self.speech = SpeechIO()
        self.reminders = queue.Queue()
        self.running = True
        threading.Thread(target=self._reminder_worker, daemon=True).start()

    def say(self, message):
        print(f"\\nAssistant: {message}")
        self.speech.speak(message)

    def _reminder_worker(self):
        while self.running:
            try:
                due, message = self.reminders.get(timeout=0.5)
                time.sleep(max(0, (due - dt.datetime.now()).total_seconds()))
                self.say(f"Reminder: {message}")
            except queue.Empty:
                continue

    def _set_reminder(self, command):
        match = re.search(r"in\\s+(\\d+)\\s+(second|seconds|minute|minutes|hour|hours)\\s+to\\s+(.+)", command)
        if match:
            amount, unit, message = int(match.group(1)), match.group(2), match.group(3).strip()
            seconds = amount * (1 if unit.startswith("second") else 60 if unit.startswith("minute") else 3600)
            due = dt.datetime.now() + dt.timedelta(seconds=seconds)
        else:
            match = re.search(r"(?:for|at)\\s+(\\d{1,2}:\\d{2})\\s+to\\s+(.+)", command)
            if not match:
                self.say("Try: remind me in 10 minutes to drink water.")
                return
            hour, minute = map(int, match.group(1).split(":"))
            now = dt.datetime.now()
            due = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if due <= now:
                due += dt.timedelta(days=1)
            message = match.group(2).strip()
        self.reminders.put((due, message))
        self.say(f"Reminder set for {due.strftime('%I:%M %p')}: {message}")

    def handle(self, command):
        if not command:
            self.say("I didn't catch that. Please try again.")
        elif any(word in command for word in ("exit", "quit", "stop assistant", "goodbye")):
            self.say("Goodbye!")
            self.running = False
        elif "help" in command:
            self.say("Try weather in a city, news, remind me in 10 minutes to drink water, time, date, open Google, or open YouTube.")
        elif "weather" in command:
            city = command.replace("weather", "").replace("in", "", 1).replace("for", "", 1).strip()
            if not city:
                city = input("Enter city: ").strip()
            self.say(get_weather(city))
        elif "news" in command or "headlines" in command:
            self.say(get_headlines())
        elif "remind me" in command or "set reminder" in command:
            self._set_reminder(command)
        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
            self.say("Opening YouTube.")
        elif "open google" in command:
            webbrowser.open("https://www.google.com")
            self.say("Opening Google.")
        elif "time" in command:
            self.say("The time is " + dt.datetime.now().strftime("%I:%M %p"))
        elif "date" in command:
            self.say("Today is " + dt.datetime.now().strftime("%A, %d %B %Y"))
        else:
            self.say("I don't recognize that command. Say help for examples.")

    def run(self):
        self.say("Hello! I am your personal voice assistant. Say help to hear commands.")
        while self.running:
            try:
                print("\\nListening... Speak now, or type if voice input is unavailable.")
                command = self.speech.listen()
                if not command:
                    command = input("You: ").strip()
                else:
                    print("You:", command)
                self.handle(command.lower().strip())
            except KeyboardInterrupt:
                self.running = False
                self.say("Assistant stopped.")
