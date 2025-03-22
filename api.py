from fastapi import FastAPI, Query 
import pandas as pd
from utils import fetch_news, analyze_sentiment, generate_tts, translate_to_hindi

# Initialize FastAPI
app = FastAPI()

# Root endpoint to check if the API is running
@app.get("/")
def root():
    return {"message": "FastAPI News Sentiment API is running!"}

# API to fetch news articles with keyword and filtering options
@app.get("/news")
def get_news(
    company: str = Query(..., description="Company name to fetch news"),
    keyword: str = Query(None, description="Keyword to filter news (e.g., 'heroic')"),
    date_filter: int = Query(None, description="Filter news from the last N days (e.g., 7 for last week)"),
    sentiment_filter: str = Query(None, description="Filter by sentiment (Positive, Negative, Neutral)")
):
    news_articles = fetch_news(company, keyword, date_filter, sentiment_filter)

    if not news_articles or all(article["title"] in ["No articles found", "Error fetching news"] for article in news_articles):
        return {"company": company, "articles": []}  # Return empty list if no news found

    return {"company": company, "articles": news_articles}

# API to analyze sentiment and generate structured report with Hindi translation
@app.post("/analyze")
def sentiment_analysis(
    company: str,
    keyword: str = None,
    date_filter: int = None,
    sentiment_filter: str = None
):
    news_articles = fetch_news(company, keyword, date_filter, sentiment_filter)

    # Handle case where no valid news articles are found
    if not news_articles or all(article["title"] in ["No articles found", "Error fetching news"] for article in news_articles):
        final_summary = f"Sorry, no relevant news found for {company}."
        hindi_summary = translate_to_hindi(final_summary)  # Translate to Hindi
        tts_filename = generate_tts(hindi_summary, "Neutral")  # Convert Hindi text to speech, sentiment in English
        return {
            "company": company,
            "articles": [],
            "comparative_analysis": {},
            "final_summary": hindi_summary,
            "structured_report": hindi_summary,
            "tts_audio": tts_filename
        }

    # Perform sentiment analysis for each news article
    for article in news_articles:
        if "title" in article and article["title"] not in ["No articles found", "Error fetching news"]:
            article["sentiment"] = analyze_sentiment(article["title"])
        else:
            article["sentiment"] = "Neutral"

    # Comparative Analysis
    df = pd.DataFrame(news_articles)
    sentiment_counts = df["sentiment"].value_counts().to_dict()

    # Determine overall sentiment
    final_sentiment = max(sentiment_counts, key=sentiment_counts.get, default="Neutral")
    final_summary = f"Overall sentiment for {company} is mostly {final_sentiment}."

    # Generate structured report
    report_text = f"Company: {company}\nOverall Sentiment: {final_sentiment}\n\nNews Articles:\n"
    for idx, article in enumerate(news_articles, start=1):
        report_text += f"{idx}. \"{article['title']}\" -> {article['sentiment']} (Date: {article['date']})\n"

    report_text += f"\nComparative Analysis:\n- Sentiment breakdown: {sentiment_counts}\n\n"
    report_text += f"Final Summary:\n{final_summary}"

    # Translate structured report to Hindi
    hindi_report = translate_to_hindi(report_text)

    # Generate Hindi TTS but keep final sentiment in English
    tts_filename = generate_tts(hindi_report, final_sentiment)

    return {
        "company": company,
        "articles": news_articles,
        "comparative_analysis": sentiment_counts,
        "final_summary": hindi_report,
        "structured_report": hindi_report,
        "tts_audio": tts_filename  # Hindi speech file with English sentiment at the end
    }
