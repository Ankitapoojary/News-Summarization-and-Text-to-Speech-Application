import streamlit as st
import feedparser
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS
from deep_translator import GoogleTranslator
import os
import nltk

# Download NLP resources
nltk.download("vader_lexicon")

# Load Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Function to fetch news articles using Google News RSS
def fetch_news(company):
    rss_url = f"https://news.google.com/rss/search?q={company}"
    feed = feedparser.parse(rss_url)

    articles = []
    for entry in feed.entries[:5]:  # Limit to 5 articles
        title = entry.title
        url = entry.link
        sentiment = analyze_sentiment(title)
        hindi_title = translate_to_hindi(title)
        articles.append({"title": title, "hindi_title": hindi_title, "url": url, "sentiment": sentiment})

    return articles if articles else [{"title": "No articles found", "hindi_title": "कोई लेख नहीं मिला", "url": "", "sentiment": "Neutral"}]

# Function to analyze sentiment
def analyze_sentiment(text):
    score = sia.polarity_scores(text)["compound"]
    return "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"

# Function to translate text to Hindi
def translate_to_hindi(text):
    return GoogleTranslator(source="auto", target="hi").translate(text)

# Function to generate Hindi TTS for all news titles
def generate_tts(articles):
    hindi_report = "न्यूज़ रिपोर्ट:\n\n"
    for i, article in enumerate(articles, 1):
        hindi_report += f"{i}. {article['hindi_title']} \nभाव: {translate_to_hindi(article['sentiment'])}\n\n"
    
    tts = gTTS(hindi_report, lang="hi")
    audio_filename = "hindi_news_report.mp3"
    tts.save(audio_filename)
    return audio_filename

# Streamlit UI
st.title("📰 News Summarization & Sentiment Analysis")

company = st.text_input("Enter Company Name:", "")

if st.button("Fetch & Analyze"):
    if company:
        articles = fetch_news(company)

        if articles and articles[0]["title"] != "No articles found":
            st.subheader("Extracted News Articles (English & Hindi)")
            for article in articles:
                st.write(f"🔹 **{article['title']}**")  # English
                st.write(f"🌐 **{article['hindi_title']}**")  # Hindi
                st.write(f"🧐 **Sentiment:** {article['sentiment']}")
                st.markdown(f"[Read more]({article['url']})")
                st.write("---")  

            # Generate Hindi TTS for all articles
            tts_file = generate_tts(articles)
            st.subheader("🔊 Hindi Audio Summary")
            st.audio(tts_file, format="audio/mp3")

        else:
            st.warning("⚠️ No news articles found.")

    else:
        st.warning("⚠️ Please enter a company name!")
