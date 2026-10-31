from django.shortcuts import render
from .sentiment import analyze_sentiment

MAX_TEXT_LENGTH = 2000

def home(request):
    context = {"text": "", "result": None, "error": None}
    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        context["text"] = text

        if not text:
            context["error"] = "Please enter some text before analyzing."
        elif len(text) > MAX_TEXT_LENGTH:
            context["error"] = f"Please keep your text under {MAX_TEXT_LENGTH} characters."
        else:
            context["result"] = analyze_sentiment(text)

    return render(request, "sentiment_app/index.html", context)
