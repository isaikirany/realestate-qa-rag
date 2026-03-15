# 🏠 Real Estate Research Tool

AI-powered real estate research tool. Paste up to 3 article URLs, ask questions, and get instant answers grounded in the source content. Built with LangChain, Groq LLM, ChromaDB, and Streamlit.

## How It Works

1. Paste up to 3 real estate article URLs in the sidebar
2. Click **Process URLs** — the app scrapes and indexes the content
3. Ask any question — the app retrieves relevant context and generates an answer with sources

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
git clone https://github.com/isaikirany/realestate-qa-rag.git
cd realestate-qa-rag
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

Open [http://localhost:8501](http://localhost:8501) in your browser.

## Deploy to Streamlit Community Cloud (free)

1. Fork or clone this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select this repo, branch `main`, file `main.py`
4. Under **Advanced settings → Secrets**, add:
```toml
GROQ_API_KEY = "your-groq-api-key-here"
```
5. Click **Deploy** — your app gets a public URL instantly
