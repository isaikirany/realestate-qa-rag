import streamlit as st
from rag import process_urls, generate_answer

st.set_page_config(
    page_title="Real Estate Research Tool",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
        /* Main background */
        .stApp { background-color: #1a1a1a; }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #111111;
            border-right: 1px solid #2e2e2e;
        }
        [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
        [data-testid="stSidebar"] .stTextInput label { color: #999999 !important; font-size: 0.8rem; }
        [data-testid="stSidebar"] input {
            background-color: #1e1e1e !important;
            border: 1px solid #3a3a3a !important;
            color: #e0e0e0 !important;
            border-radius: 6px !important;
        }
        [data-testid="stSidebar"] input:focus {
            border-color: #e8632a !important;
        }

        /* Process button */
        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            background-color: #e8632a;
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: background-color 0.2s;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: #cf5522;
        }

        /* Answer card */
        .answer-card {
            background: #242424;
            border-radius: 12px;
            padding: 1.5rem 2rem;
            border-left: 4px solid #e8632a;
            box-shadow: 0 2px 12px rgba(0,0,0,0.4);
            margin-top: 1rem;
            color: #e0e0e0;
            line-height: 1.7;
        }

        /* Sources card */
        .sources-card {
            background: #1e1e1e;
            border: 1px solid #2e2e2e;
            border-radius: 10px;
            padding: 1rem 1.5rem;
            margin-top: 1rem;
        }
        .sources-card a {
            color: #e8632a;
            word-break: break-all;
            font-size: 0.88rem;
            text-decoration: none;
        }
        .sources-card a:hover { text-decoration: underline; }

        /* Hero title */
        .hero-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.2rem;
        }
        .hero-title span { color: #e8632a; }
        .hero-sub {
            color: #888888;
            font-size: 1rem;
            margin-bottom: 2rem;
        }

        /* Section labels */
        .section-label {
            color: #e8632a;
            font-weight: 600;
            font-size: 0.85rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }

        /* Question input */
        .stTextInput input {
            background-color: #242424 !important;
            border-radius: 8px !important;
            border: 1.5px solid #3a3a3a !important;
            color: #e0e0e0 !important;
            font-size: 1rem !important;
        }
        .stTextInput input:focus {
            border-color: #e8632a !important;
            box-shadow: 0 0 0 3px rgba(232,99,42,0.15) !important;
        }
        .stTextInput input::placeholder { color: #666666 !important; }

        /* Divider */
        hr { border-color: #2e2e2e; }

        /* Override Streamlit text colors in main area */
        .stApp p, .stApp li, .stApp label { color: #cccccc; }
        .stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: #ffffff; }

        /* Alert boxes */
        [data-testid="stAlert"] { border-radius: 8px !important; }

        /* Hide Streamlit default elements */
        #MainMenu, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏠 Real Estate RAG")
    st.markdown("---")
    st.markdown("#### Paste article URLs below")

    url1 = st.text_input("URL 1", placeholder="https://...")
    url2 = st.text_input("URL 2", placeholder="https://...")
    url3 = st.text_input("URL 3", placeholder="https://...")

    st.markdown("")
    process_url_button = st.button("⚡ Process URLs")

    st.markdown("---")
    st.markdown(
        "<small style='color:#555555'>Powered by LangChain · Groq · ChromaDB</small>",
        unsafe_allow_html=True,
    )

# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🏠 Real Estate <span>Research Tool</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Paste real-estate article URLs, then ask any question about them.</div>', unsafe_allow_html=True)
st.markdown("---")

status_placeholder = st.empty()

# Steps match the yield statements in rag.py
PROCESS_STEPS = [
    "initializing components",
    "load data",
    "split data into chunks",
    "add docs to vector db",
]

# Process URLs
if process_url_button:
    urls = [u for u in (url1, url2, url3) if u.strip()]
    if not urls:
        status_placeholder.error("Please enter at least one URL in the sidebar.")
    else:
        progress_bar = st.progress(0, text="Starting…")
        step_label = st.empty()
        for status in process_urls(urls):
            step = status.lower().strip()
            pct = (PROCESS_STEPS.index(step) + 1) / len(PROCESS_STEPS) if step in PROCESS_STEPS else 0
            progress_bar.progress(pct, text=f"Step {int(pct * len(PROCESS_STEPS))}/{len(PROCESS_STEPS)} — {status.capitalize()}…")
            step_label.markdown(f"<small style='color:#888'>⏳ {status.capitalize()}…</small>", unsafe_allow_html=True)
        progress_bar.progress(1.0, text="Done!")
        step_label.empty()
        status_placeholder.success(f"✅ Successfully processed {len(urls)} URL(s). You can now ask questions below.")

# Question & Answer
st.markdown("#### Ask a Question")
query = st.text_input("", placeholder="e.g. What is the current state of the housing market?", label_visibility="collapsed")

if query:
    try:
        with st.spinner("Generating answer…"):
            answer, sources = generate_answer(query)

        st.markdown("**Answer**")
        st.markdown(f'<div class="answer-card">{answer}</div>', unsafe_allow_html=True)

        if sources:
            st.markdown("")
            st.markdown("**Sources**")
            source_links = "".join(
                f'<div style="margin-bottom:4px">🔗 <a href="{s.strip()}" target="_blank">{s.strip()}</a></div>'
                for s in sources.split(",") if s.strip()
            )
            st.markdown(f'<div class="sources-card">{source_links}</div>', unsafe_allow_html=True)

    except RuntimeError:
        status_placeholder.error("⚠️ Please process at least one URL before asking a question.")
