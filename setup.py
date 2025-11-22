from setuptools import setup, find_packages

setup(
    name="sl_market_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "groq",
        "openai",
        "beautifulsoup4",
        "requests",
        "selenium",
        "chromadb",
        "sentence-transformers",
        "python-dotenv",
        "pydantic",
    ],
    python_requires=">=3.8",
    author="Your Name",
    description="An intelligent market analysis agent",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
