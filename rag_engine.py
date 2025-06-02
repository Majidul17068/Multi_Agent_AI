import os
from typing import List
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from utils.config import VECTOR_DB_DIR


# Initialize the embedding model
embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def create_vector_db_from_text(text: str) -> Chroma:
    """
    Split text into chunks, embed, and create Chroma vector store.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.create_documents([text])

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedder,
        persist_directory=VECTOR_DB_DIR,
    )

    vectordb.persist()
    return vectordb


def create_vector_db_from_documents(docs: List[Document]) -> Chroma:
    """
    Use if you already have a list of LangChain Document objects.
    """
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedder,
        persist_directory=VECTOR_DB_DIR,
    )

    vectordb.persist()
    return vectordb


def load_vector_db() -> Chroma:
    """
    Load a persisted Chroma vector DB from disk.
    """
    return Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embedder)


def query_vector_db(query: str, k: int = 5) -> List[Document]:
    """
    Search for top-k similar documents from the vector DB.
    """
    vectordb = load_vector_db()
    results = vectordb.similarity_search(query, k=k)
    return results


def get_context_from_query(query: str, k: int = 5) -> str:
    """
    Return joined context string from top-k similarity matches.
    """
    docs = query_vector_db(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])
