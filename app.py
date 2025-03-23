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
    for entry in feed.entries[:10]:  # Limit to minimum of 10 articles
        title = entry.title
        url = entry.link
        sentiment = analyze_sentiment(title)
        hindi_title = translate_to_hindi(title)
        articles.append({"title": title, "hindi_title": hindi_title, "url": url, "sentiment": sentiment})

    return articles if articles else [{"title": "No articles found", "hindi_title": "\u0915\u094b\u0908 \u0932\u0947\u0916 \u0928\u0939\u0940\u0902 \u092e\u093f\u0932\u093e", "url": "", "sentiment": "Neutral"}]

# Function to analyze sentiment
def analyze_sentiment(text):
    score = sia.polarity_scores(text)["compound"]
    return "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"

# Function to translate text to Hindi
def translate_to_hindi(text):
    return GoogleTranslator(source="auto", target="hi").translate(text)

# Function to generate Hindi TTS for all news titles
def generate_tts(articles):
    hindi_report = "\u0928\u094D\u092F\u0942\u091C\u093C \u0930\u093F\u092A\u094B\u0930\u094D\u091F:\n\n"
    for i, article in enumerate(articles, 1):
        hindi_report += f"{i}. {article['hindi_title']} \n\u092D\u093E\u0935: {translate_to_hindi(article['sentiment'])}\n\n"
    
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

