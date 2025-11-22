# 🚀 Quick Start Guide

## Run the Terminal App
```bash
python app.py
```

## Run the Web App
```bash
streamlit run web_app.py
```
The web interface will automatically open at `http://localhost:8501`

## Deploy to GitHub

### 1. Create GitHub Repository
- Go to https://github.com/new
- Name: `sl-market-agent`
- Keep it public or private
- DON'T initialize with README (we already have one)

### 2. Initialize Git & Push
```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: SL Market Intelligence Agent"

# Add your GitHub repo
git remote add origin https://github.com/Isuruigi/sl-market-agent.git

# Push
git branch -M main
git push -u origin main
```

### 3. Verify
Your project is now on GitHub! 🎉

## Important Notes
- ⚠️ The `.env` file is NOT uploaded (protected by `.gitignore`)
- ✅ Your API keys remain secure on your local machine
- 📝 Update the GitHub URL in README.md and web_app.py with your actual username

## Next Steps
- Share your repo link
- Add a screenshot to README.md  
- Deploy to Streamlit Cloud (free!)
- Add more Sri Lankan market data

---

**That's it! Your project is complete and ready to share!** 🚀
