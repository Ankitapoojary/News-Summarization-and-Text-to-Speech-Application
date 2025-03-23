---
title: "News-Summarization-and-Text-to-Speech-Application"
sdk: "streamlit"
app_file: "app.py"
---

# 📰 News Summarization & Text-to-Speech (TTS) Application

## 📌 Project Overview
This application extracts news related to a company, performs sentiment analysis, and generates a Hindi TTS report.

## 📂 Project Structure
# **Project Documentation**  

## **1. Project Setup**  
### **Installation Steps:**  
1. Install Python (version 3.8 or later).  
2. Install required dependencies:  
   ```bash
   pip install fastapi uvicorn streamlit nltk gtts deep-translator feedparser requests
   ```
3. Download the necessary NLTK resources:  
   ```python
   import nltk
   nltk.download("vader_lexicon")
   ```
4. Run the FastAPI server:  
   ```bash
   uvicorn api:app --reload
   ```
5. Open the browser and test the API.  

6. Run the Streamlit application:  
   ```bash
   streamlit run app.py
   ```

---

## **2. Model Details**  
- **Sentiment Analysis:** Uses NLTK's VADER sentiment analysis to classify news articles as Positive, Negative, or Neutral.  
- **Text Summarization:** Not explicitly implemented but provides structured analysis of news articles.  
- **Text-to-Speech (TTS):** Uses Google Text-to-Speech (gTTS) to convert the summary to an audio file in Hindi.  

---

## **3. API Development**  
- The FastAPI backend provides endpoints for fetching news and analyzing sentiment.  
- APIs can be accessed via a browser by entering the respective URLs.  

### **Endpoints:**  
1. **Root Endpoint:**  
   - **URL:** `http://127.0.0.1:8000/`  
   - **Purpose:** Check if the API is running.  

2. **Fetch News:**  
   - **URL:** `http://127.0.0.1:8000/news?company=Tesla`  
   - **Parameters:**  
     - `company`: Required (e.g., "Tesla")  
     - `keyword`: Optional filter (e.g., "EV")  
     - `date_filter`: Optional filter (e.g., last 7 days)  
     - `sentiment_filter`: Optional filter (Positive, Negative, Neutral)  
   - **Purpose:** Fetch news articles related to a company with optional filtering.  

3. **Sentiment Analysis:**  
   - **URL:** `http://127.0.0.1:8000/analyze`  
   - **Method:** POST (Use a browser extension to send POST requests).  
   - **Parameters:**  
     - `company`: Required (e.g., "Apple")  
     - `keyword`, `date_filter`, `sentiment_filter`: Optional  
   - **Purpose:** Analyzes news sentiment and provides a structured summary.  

---

## **4. API Usage**  
- **Google News RSS:** Fetches news articles based on the company name.  
- **Google Translate:** Translates news summaries into Hindi.  
- **Google Text-to-Speech (gTTS):** Converts text summaries to Hindi speech.  

---

## **5. Assumptions & Limitations**  
- The application depends on Google News RSS, which may not always return relevant or sufficient articles.  
- Sentiment analysis is based only on headlines, which may not always reflect the true sentiment of the article.  
- Google Translate and gTTS require an internet connection.  
- No database is used; data is processed in real-time.  

---

This documentation provides a simple overview of the project, including installation, API details, and dependencies. Let me know if you need modifications! 🚀
