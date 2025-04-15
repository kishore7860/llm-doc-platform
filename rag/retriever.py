from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_document(text: str, chunk_size: int = 500, chunk_overlap: int = 50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

def build_vector_index(chunks: list[str], persist_dir: str = "rag_index") -> Chroma:
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_texts(chunks, embeddings, persist_directory=persist_dir)
    db.persist()
    return db

def query_vector_index(query: str, persist_dir: str = "rag_index"):
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return db.similarity_search(query, k=5)