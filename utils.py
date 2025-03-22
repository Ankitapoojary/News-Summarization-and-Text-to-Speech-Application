import requests
import nltk
import feedparser
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import os
from deep_translator import GoogleTranslator
from datetime import datetime

# Load Sentiment Analyzer
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

# Function to fetch news articles using Google News RSS
def fetch_news(company, keyword=None, date_filter=None, sentiment_filter=None):
    try:
        rss_url = f"https://news.google.com/rss/search?q={company}"
        feed = feedparser.parse(rss_url)

        articles = []
        for entry in feed.entries[:10]:  # Get first 10 articles
            article_date = datetime(*entry.published_parsed[:6]) if "published_parsed" in entry else None
            title = entry.title
            url = entry.link

            # Keyword filtering
            if keyword and keyword.lower() not in title.lower():
                continue

            # Date filtering (only applies if a date filter is provided)
            if date_filter:
                days_ago = (datetime.now() - article_date).days if article_date else None
                if days_ago is not None and days_ago > date_filter:
                    continue

            # Sentiment Analysis
            sentiment = analyze_sentiment(title)

            # Sentiment filtering
            if sentiment_filter and sentiment != sentiment_filter:
                continue

            articles.append({"title": title, "url": url, "date": article_date.strftime("%Y-%m-%d") if article_date else "Unknown", "sentiment": sentiment})

        return articles if articles else [{"title": "No articles found", "url": "", "date": "Unknown", "sentiment": "Neutral"}]

    except Exception as e:
        print(f"Error fetching news: {e}")
        return [{"title": "Error fetching news", "url": "", "date": "Unknown", "sentiment": "Neutral"}]

# Function to analyze sentiment
def analyze_sentiment(text):
    try:
        score = sia.polarity_scores(text)["compound"]
        if score > 0.05:
            return "Positive"
        elif score < -0.05:
            return "Negative"
        else:
            return "Neutral"
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return "Neutral"

# Function to translate text to Hindi
def translate_to_hindi(text):
    try:
        return GoogleTranslator(source="auto", target="hi").translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails

# Function to generate Hindi TTS with final sentiment in English
def generate_tts(text, final_sentiment, filename="report_audio.mp3"):
    try:
        hindi_text = translate_to_hindi(text)  # Translate full report to Hindi
        final_audio_text = hindi_text + f"\nOverall Sentiment: {final_sentiment}"  # Append sentiment in English
        tts = gTTS(final_audio_text, lang="hi")  # Convert to Hindi speech
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"TTS generation error: {e}")
        return None
