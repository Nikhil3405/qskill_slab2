# Sentiment Analysis Web Application

A Django web application that classifies user-entered English text as Positive, Negative or Neutral using TextBlob.

## Features
- Text input with character limit and sample prompts.
- Sentiment label: Positive, Negative or Neutral.
- Polarity score (-1 to +1).
- Subjectivity score (0 to 1).
- Responsive interface and CSRF-protected Django form.

## Tech stack
Python, Django, TextBlob, HTML, CSS and JavaScript.

## Setup
Python 3.10+ recommended.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\\Scripts\\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install and run:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## How it works
TextBlob returns polarity and subjectivity scores. This app applies a simple threshold:
- polarity > 0.1: Positive
- polarity < -0.1: Negative
- otherwise: Neutral

Polarity measures sentiment orientation. Subjectivity estimates whether the text is opinion-like rather than factual.

## Limitations
This is a basic lexicon-based sentiment analyzer for English. It may not correctly interpret sarcasm, slang, mixed sentiment, domain-specific language or context. The thresholds are simple educational rules, not universal standards. Do not treat the output as a definitive judgment about a person or customer.
