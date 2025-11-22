# ☁️ Deploying to Streamlit Cloud

Deploying your **SL Market Agent** to the web is free and easy with Streamlit Cloud.

## Prerequisites
1.  Your code must be on GitHub (✅ Done!)
2.  You need a [Streamlit Community Cloud](https://streamlit.io/cloud) account.

## Step-by-Step Guide

### 1. Prepare Your Repo
Ensure you have:
-   `web_app.py` (Main app file)
-   `requirements.txt` (Dependencies)
-   `.gitignore` (To exclude local secrets)

### 2. Connect to Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"New app"**.
3.  Select **"Use existing repo"**.
4.  Choose your repository: `Isuruigi/sl-market-agent`.
5.  **Branch:** `main`
6.  **Main file path:** `web_app.py`

### 3. Configure Secrets (IMPORTANT!)
Your app needs your API keys to work. Since we didn't upload `.env` to GitHub, you must add them manually in Streamlit.

1.  Click **"Advanced settings"**.
2.  Find the **"Secrets"** field.
3.  Paste your secrets in TOML format:

```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
LANGSMITH_API_KEY = "lsv2_your_actual_key_here"
LANGCHAIN_TRACING_V2 = "true"
LANGCHAIN_PROJECT = "sl-market-agent"
```

### 4. Deploy! 🚀
1.  Click **"Deploy"**.
2.  Wait a few minutes for the build to finish.
3.  **Success!** Your app is now live at `https://sl-market-agent.streamlit.app` (or similar).

## Troubleshooting

-   **"Module not found"**: Check `requirements.txt`. Ensure all libraries are listed.
-   **"API Key Error"**: Double-check your Secrets in the Streamlit dashboard.
-   **"App crashes"**: Check the logs in the bottom right corner of the Streamlit app.

---

**Enjoy your live AI Agent!** 🌍
