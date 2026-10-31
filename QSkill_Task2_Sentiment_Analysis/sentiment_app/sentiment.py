from textblob import TextBlob

def analyze_sentiment(text: str) -> dict:
    """Return TextBlob polarity, subjectivity and a simple sentiment label."""
    blob = TextBlob(text)
    polarity = float(blob.sentiment.polarity)
    subjectivity = float(blob.sentiment.subjectivity)

    # Thresholds are a simple educational rule, not a universal language standard.
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "label": label,
        "polarity": polarity,
        "subjectivity": subjectivity,
    }
