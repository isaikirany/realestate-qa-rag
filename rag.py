import os
from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# On Streamlit Cloud, secrets override .env
try:
    import streamlit as st
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass
CHUNK_SIZE = 1000
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = 'real_estate'

llm = None
vector_store = None

def initialize_components():
    global llm, vector_store

    if llm is None:
        llm = ChatGroq(model='compound-beta-mini', temperature=0.9, max_tokens=500)

    if vector_store is None:
        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR)
        )

def process_urls(urls):
    """
    This function scrapes data from urls and stores it in a vector db
    :param urls: input urls
    """
    yield "initializing components"
    initialize_components()

    vector_store.reset_collection()

    yield 'load data'
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()

    yield 'split data into chunks'
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', ' '],
        chunk_size=CHUNK_SIZE
    )

    docs = text_splitter.split_documents(data)

    uuids = [str(uuid4()) for _ in range(len(docs))]
    yield 'add docs to vector db'
    vector_store.add_documents(docs, ids=uuids)

def generate_answer(query):
    """
    This function generates an answer for a given query using the vector db and llm
    :param query: input query
    :return: answer from llm, sources
    """
    if not vector_store:
        raise RuntimeError("Vector store is not initialized. Please run process_urls first.")

    prompt = ChatPromptTemplate.from_template(
        "Answer the question based on the context below.\n\nContext:\n{context}\n\nQuestion: {question}"
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def get_sources(docs):
        return ", ".join({doc.metadata.get("source", "") for doc in docs if doc.metadata.get("source")})

    retriever = vector_store.as_retriever()
    retrieved_docs = retriever.invoke(query)

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": format_docs(retrieved_docs), "question": query})
    sources = get_sources(retrieved_docs)

    return answer, sources

if __name__ == "__main__":

    urls = ['https://www.cnbc.com/2026/03/11/weekly-mortgage-demand-from-homebuyers-increased-despite-big-interest-rate-volatility.html',
    'https://www.cnbc.com/2026/03/10/february-home-sales-see-small-rebound-but-supply-growth-is-sluggish.html']

    process_urls(urls)

    answer, sources = generate_answer("What is the current state of the real estate market?")
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")
