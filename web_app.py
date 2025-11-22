"""Web Interface using Streamlit for SL Market Intelligence Agent"""

import streamlit as st
from src.agent.market_agent import MarketAgent

# Page config
st.set_page_config(
    page_title="SL Market Intelligence",
    page_icon="🇱🇰",
    layout="wide"
)

# Title
st.title("🇱🇰 Sri Lankan Market Intelligence Agent")
st.markdown("Ask me about Sri Lankan economy, news, and market data!")

# Initialize agent (with caching so it doesn't reload every time)
@st.cache_resource
def load_agent():
    """Load and initialize the market agent."""
    agent = MarketAgent(verbose=False)
    # Add initial knowledge
    agent.add_knowledge([
        "Sri Lanka's GDP is approximately $75 billion.",
        "Main exports: tea, textiles, rubber, spices.",
        "Currency: Sri Lankan Rupee (LKR).",
        "Central Bank of Sri Lanka manages monetary policy.",
        "The Colombo Stock Exchange (CSE) is the main stock exchange.",
        "Tourism is a major contributor to the economy.",
    ])
    return agent

# Load agent
try:
    from src.config import Config
    Config.validate()
    agent = load_agent()
except ValueError as e:
    st.error("⚙️ Configuration Error")
    st.warning("Your API keys are missing or invalid.")
    
    st.markdown("""
    ### 🛠️ How to Fix on Streamlit Cloud
    
    1. Go to your app dashboard
    2. Click **Settings** (top right) -> **Secrets**
    3. Paste your keys like this:
    
    ```toml
    GROQ_API_KEY = "gsk_..."
    LANGSMITH_API_KEY = "lsv2_..."
    ```
    
    [See Deployment Guide](https://github.com/Isuruigi/sl-market-agent/blob/main/DEPLOYMENT.md)
    """)
    st.stop()
except Exception as e:
    st.error(f"❌ Failed to initialize agent: {e}")
    st.stop()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about Sri Lankan markets..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                response = agent.chat(prompt)
                st.markdown(response)
                # Add assistant response to chat
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar
with st.sidebar:
    st.header("📊 Features")
    st.markdown("""
    - 📰 Web scraping capabilities
    - 🧮 Financial calculations (AST-based)
    - 📚 Knowledge base with semantic search
    - 💬 Conversation memory
    - 🔄 Retry logic for reliability
    """)
    
    st.header("🛠️ Available Tools")
    tools = agent.get_tools_info()
    for tool in tools:
        st.markdown(f"**{tool['name']}**: {tool['description'][:50]}...")
    
    st.header("⚙️ Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧹 Clear Chat"):
            st.session_state.messages = []
            agent.reset()
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Knowledge"):
            agent.clear_knowledge()
            st.success("Knowledge base cleared!")
    
    # Add knowledge section
    st.header("📝 Add Knowledge")
    knowledge_text = st.text_area(
        "Add custom knowledge:",
        placeholder="Enter information about Sri Lankan markets...",
        height=100
    )
    if st.button("➕ Add to Knowledge Base"):
        if knowledge_text:
            agent.add_knowledge([knowledge_text])
            st.success("✅ Knowledge added successfully!")
        else:
            st.warning("Please enter some text first.")
    
    # Stats
    st.header("📈 Statistics")
    st.metric("Knowledge Items", agent.rag.count())
    st.metric("Chat Messages", len(st.session_state.messages))

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ using [Streamlit](https://streamlit.io) • "
    "Powered by [Groq](https://groq.com) • "
    "[GitHub](https://github.com/Isuruigi/sl-market-agent)"
)
