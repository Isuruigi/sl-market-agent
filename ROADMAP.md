# 🗺️ Implementation Roadmap for Future Enhancements

Here is a guide on how to implement the requested features for the Sri Lankan Market Intelligence Agent.

## 1. ✅ Streamlit Web Interface
**Status:** *Already Implemented!*
You have `web_app.py`. To run it:
```bash
streamlit run web_app.py
```
**Enhancements:**
- Add more tabs for specific data views.
- Deploy to [Streamlit Cloud](https://streamlit.io/cloud) for free hosting.

## 2. 📰 Real-time Sri Lankan News Integration
**Goal:** Fetch live news instead of just scraping one URL.

**Approach:**
1.  **RSS Feeds:** Many SL news sites (Ada Derana, Daily Mirror) have RSS feeds.
    - *Library:* `feedparser`
2.  **News API:** Use a news aggregator API filtering for "Sri Lanka" + "Economy".
    - *Library:* `newsapi-python`
3.  **Custom Scraper:** Build a scheduled scraper for `DailyFT.lk` or `LankaBusinessOnline`.

**Code Snippet (RSS):**
```python
import feedparser
def get_sl_news():
    feed = feedparser.parse("http://www.adaderana.lk/rss.php")
    return [entry.title for entry in feed.entries[:5]]
```

## 3. 📈 Advanced Financial Analytics
**Goal:** Analyze trends, not just retrieve text.

**Approach:**
1.  **Data Source:** Scrape Colombo Stock Exchange (CSE) data or use an API if available.
2.  **Analysis:** Use `pandas` for data manipulation.
3.  **Metrics:** Calculate:
    - Year-over-Year (YoY) growth
    - Inflation adjustments
    - Stock performance metrics (PE Ratio, RSI)

**Code Snippet:**
```python
import pandas as pd
def analyze_growth(current, previous):
    return ((current - previous) / previous) * 100
```

## 4. 📊 Data Visualization Dashboards
**Goal:** Visual charts for GDP, inflation, stock prices.

**Approach:**
1.  **Library:** Use `Plotly` (interactive) or `Matplotlib`.
2.  **Integration:** Streamlit supports these natively.

**Code Snippet (Streamlit + Plotly):**
```python
import plotly.express as px
data = {'Year': [2020, 2021, 2022], 'GDP Growth': [-3.6, 3.7, -7.8]}
fig = px.line(data, x='Year', y='GDP Growth', title='SL GDP Growth')
st.plotly_chart(fig)
```

## 5. 🔌 REST API Deployment
**Goal:** Allow other apps (mobile, web) to talk to your agent.

**Approach:**
1.  **Framework:** Use `FastAPI` (modern, fast).
2.  **Endpoints:** `/chat`, `/news`, `/calculate`.
3.  **Deployment:** Host on Render, Railway, or AWS.

**Code Snippet (FastAPI):**
```python
from fastapi import FastAPI
app = FastAPI()
agent = MarketAgent()

@app.post("/chat")
def chat(query: str):
    return {"response": agent.chat(query)}
```

## 6. 🗣️ Multi-language Support (Sinhala, Tamil)
**Goal:** Chat in local languages.

**Approach:**
1.  **LLM Native:** The Llama-3 model already understands some Sinhala/Tamil. Update the system prompt: *"You can reply in Sinhala or Tamil if asked."*
2.  **Translation Layer:** Use `googletrans` or `deep_translator` to translate User Input -> English -> LLM -> English Response -> Sinhala/Tamil.

**Code Snippet (Prompt Engineering):**
```python
system_prompt += " If the user asks in Sinhala, reply in Sinhala. If in Tamil, reply in Tamil."
```

## 7. 📱 Mobile App
**Goal:** Access agent from phone.

**Approach:**
1.  **Easiest:** The Streamlit app (`web_app.py`) is **already mobile responsive**! Just deploy it and open the URL on your phone.
2.  **Native App:** Build with **Flutter** or **React Native**.
    - Needs the **REST API** (Step 5) to communicate.

---

### Recommended Order of Execution
1.  **News Integration** (High value, easy)
2.  **Data Viz** (Great for Streamlit)
3.  **REST API** (If you want to build a mobile app later)
