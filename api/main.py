from ingestion.text_extractor import extract_text
from ingestion.metadata_extractor import extract_basic_metadata
from rag.retriever import chunk_document, build_vector_index, query_vector_index
from analysis.ner import extract_entities
from analysis.summarizer import summarize

@app.post("/ingest/")
async def ingest_file(file: UploadFile):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)
    metadata = extract_basic_metadata(file_path)
    chunks = chunk_document(text)
    build_vector_index(chunks)

    return {"message": "Document indexed", "metadata": metadata, "chunks": len(chunks)}

@app.get("/search/")
def search_docs(q: str):
    results = query_vector_index(q)
    return {"results": [doc.page_content for doc in results]}


@app.post("/analyze/")
async def analyze_file(file: UploadFile):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)
    entities = extract_entities(text)
    summary = summarize(text)

    return {
        "summary": summary,
        "entities": entities[:20]  # Return first 20 entities for brevity
    }