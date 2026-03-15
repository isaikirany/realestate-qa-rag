# 🏠 Real Estate Research Tool

A RAG (Retrieval-Augmented Generation) app that lets you paste real-estate article URLs and ask questions about them — powered by LangChain, Groq, and ChromaDB.

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | [Groq](https://groq.com) (`compound-beta-mini`) |
| Embeddings | HuggingFace `BAAI/bge-base-en-v1.5` |
| Vector Store | ChromaDB |
| Framework | LangChain |
| UI | Streamlit |

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

**2. Create and activate a virtual environment**
```bash
python -m venv env
source env/Scripts/activate   # Windows
# source env/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your Groq API key**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your-groq-api-key-here
```
Get a free key at [console.groq.com](https://console.groq.com).

**5. Run the app**
```bash
streamlit run main.py
```

## Deploy to Streamlit Community Cloud (free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub account
3. Select this repo → set **Main file** to `main.py`
4. Under **Advanced settings → Secrets**, add:
```toml
GROQ_API_KEY = "your-groq-api-key-here"
```
5. Click **Deploy** — your app gets a public URL instantly
