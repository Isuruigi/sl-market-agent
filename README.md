# 🇱🇰 Sri Lankan Market Intelligence Agent

AI-powered assistant for Sri Lankan economic analysis and market intelligence with production-ready components.

## ✨ Features

- 🧮 **Financial Calculations** - Safe AST-based calculator (no eval)
- 🌐 **Web Scraping** - Extract content from any URL
- 📚 **Knowledge Base** - RAG with semantic search using sentence transformers
- 💬 **Conversational AI** - Memory-enabled intelligent responses
- 🛠️ **Tool Calling** - Automatic tool selection (Calculator, WebScraper, Knowledge Search)
- 🔄 **Retry Logic** - Exponential backoff for resilience
- 📊 **LangSmith Monitoring** - Optional observability (free tier)

## 🚀 Tech Stack

- **LLM:** Groq (llama-3.3-70b-versatile) with retry logic
- **Framework:** Production-ready Python with LangChain components
- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Store:** Numpy + Pickle (simple & fast)
- **Calculator:** AST parsing (secure, no eval)
- **Memory:** Deque-based conversation buffer
- **Monitoring:** LangSmith (optional)

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/Isuruigi/sl-market-agent.git
cd sl-market-agent

# Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

### Get API Keys

1. **GROQ API Key** (Required)
   - Visit: https://console.groq.com/keys
   - Create account and generate API key

2. **LangSmith API Key** (Optional - for monitoring)
   - Visit: https://smith.langchain.com/settings
   - Free tier available

### Set Up Environment

Create `.env` file in project root:

```env
# Required
GROQ_API_KEY=gsk_your_actual_groq_api_key_here

# Optional - LangSmith Monitoring
LANGSMITH_API_KEY=lsv2_your_langsmith_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=sl-market-agent
```

## 🎮 Usage

### Terminal App

```bash
python app.py
```

**Available Commands:**
- `/help` - Show all commands
- `/tools` - List available tools
- `/add` - Add knowledge to the system
- `/clear` - Clear knowledge base
- `/reset` - Reset conversation history
- `/verbose` - Toggle detailed logging
- `/quit` - Exit application

### Example Interactions

```bash
You: What is 25% of 10000?
Agent: Result: 2500

You: /add
# Add custom knowledge about Sri Lankan markets

You: What are the main exports?
Agent: [Searches knowledge base and provides answer]
```

## 📁 Project Structure

```
sl_market_agent/
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   └── market_agent.py      # Main agent with tool calling
│   ├── llm/
│   │   ├── __init__.py
│   │   └── groq_llm.py           # LLM with retry logic
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── calculator.py         # AST-based safe calculator
│   │   ├── web_scraper.py        # Web content extraction
│   │   └── tools_registry.py    # Tools management
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── conversation_memory.py # Deque-based memory
│   │   └── vector_store.py       # RAG with numpy
│   └── config.py                 # Configuration & validation
├── data/
│   └── vector_store/             # Persisted embeddings
├── tests/
│   ├── test_llm.py
│   ├── test_tools.py
│   └── test_agent.py
├── .env                          # Environment variables (create this)
├── .gitignore
├── app.py                        # Terminal interface
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
└── README.md                     # This file
```

## 🔧 Component Tests

Test individual components:

```bash
# Test configuration
python -c "from src.config import Config; print('✅ Config OK')"

# Test LLM
python -m src.llm.groq_llm

# Test calculator
python -m src.tools.calculator

# Test memory
python -m src.memory.conversation_memory
python -m src.memory.vector_store

# Test agent
python -m src.agent.market_agent
```

## 🌟 Key Features

### 1. Safe Calculator
- **AST Parsing** - No `eval()`, prevents code injection
- **Supported Operations** - `+`, `-`, `*`, `/`, `**`, parentheses
- **Auto-formatting** - Handles `^`, `×`, `÷` symbols

### 2. Intelligent Agent
- **Tool Selection** - Automatically chooses right tool for the task
- **Context-Aware** - Uses conversation history and RAG
- **Error Handling** - Graceful degradation with retries

### 3. Production-Ready
- **Retry Logic** - 3 attempts with exponential backoff
- **API Validation** - Checks key format before use
- **Logging** - Optional verbose mode for debugging
- **Persistence** - Vector store saves to disk

## 🚧 Future Enhancements

- [ ] Streamlit web interface
- [ ] Real-time Sri Lankan news integration
- [ ] Advanced financial analytics
- [ ] Data visualization dashboards
- [ ] REST API deployment
- [ ] Multi-language support (Sinhala, Tamil)
- [ ] Mobile app

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author

**Isuru Pathirana**
- GitHub: [@Isuruigi](https://github.com/Isuruigi)

## 🙏 Acknowledgments

- Groq for lightning-fast LLM inference
- LangChain for framework components  
- Sentence Transformers for embeddings
- The open-source community

---

**Note:** This is a production-ready implementation prioritizing simplicity, security, and reliability over complex frameworks.
