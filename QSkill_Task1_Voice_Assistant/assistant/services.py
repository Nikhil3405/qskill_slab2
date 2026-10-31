import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

def _json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "QSkillVoiceAssistant/1.0"})
    with urllib.request.urlopen(req, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))

def get_weather(city):
    if not city:
        return "Please provide a city, for example: weather in Bengaluru."
    try:
        data = _json("https://geocoding-api.open-meteo.com/v1/search?name="
                     + urllib.parse.quote(city) + "&count=1&language=en&format=json")
        places = data.get("results", [])
        if not places:
            return f"I couldn't find {city}."
        place = places[0]
        weather = _json("https://api.open-meteo.com/v1/forecast"
                        f"?latitude={place['latitude']}&longitude={place['longitude']}"
                        "&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m")
        current = weather.get("current", {})
        return (f"In {place['name']}, it is {current.get('temperature_2m', 'unknown')} degrees Celsius. "
                f"It feels like {current.get('apparent_temperature', 'unknown')} degrees, "
                f"humidity is {current.get('relative_humidity_2m', 'unknown')} percent, "
                f"and wind speed is {current.get('wind_speed_10m', 'unknown')} kilometres per hour.")
    except Exception as exc:
        return f"Weather service unavailable: {exc}"

def get_headlines(limit=5):
    try:
        req = urllib.request.Request("https://feeds.bbci.co.uk/news/world/rss.xml",
                                     headers={"User-Agent": "QSkillVoiceAssistant/1.0"})
        with urllib.request.urlopen(req, timeout=12) as response:
            root = ET.fromstring(response.read())
        titles = [item.findtext("title", "").strip()
                  for item in root.findall("./channel/item")[:limit]]
        titles = [title for title in titles if title]
        if not titles:
            return "No headlines were returned."
        return "Here are the latest world headlines. " + " ".join(
            f"Headline {i}: {title}." for i, title in enumerate(titles, 1))
    except Exception as exc:
        return f"News service unavailable: {exc}"
