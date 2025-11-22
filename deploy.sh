"""Simple deployment script for GitHub"""

# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: SL Market Intelligence Agent

- Production-ready market analysis agent
- LLM: Groq (llama-3.3-70b-versatile) with retry logic
- Tools: Calculator (AST), Web Scraper, Knowledge Search
- Memory: Deque-based conversation buffer
- RAG: Numpy + Sentence Transformers
- Interfaces: Terminal CLI + Streamlit web app
- Monitoring: LangSmith integration (optional)"

# Add remote (replace with your GitHub repo URL)
# git remote add origin https://github.com/YOUR_USERNAME/sl-market-agent.git

# Push to GitHub
# git branch -M main
# git push -u origin main

echo "✅ Ready to push to GitHub!"
echo ""
echo "Next steps:"
echo "1. Create a new repository on GitHub"
echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/sl-market-agent.git"
echo "3. Run: git branch -M main"
echo "4. Run: git push -u origin main"
