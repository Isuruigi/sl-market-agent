from setuptools import setup, find_packages

setup(
    name="sl_market_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "groq>=0.4.0",
        "python-dotenv",
        "requests",
        "beautifulsoup4",
        "pydantic>=2.0.0",
        "streamlit>=1.29.0",
    ],
    python_requires=">=3.9",
    author="Isuru Pathirana",
    description="Sri Lankan Market Intelligence Agent",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
