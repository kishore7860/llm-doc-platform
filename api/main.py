from ingestion.text_extractor import extract_text
from ingestion.metadata_extractor import extract_basic_metadata
from rag.retriever import chunk_document, build_vector_index, query_vector_index
from analysis.ner import extract_entities
from analysis.summarizer import summarize
from analysis.relationship_mapper import extract_relationships
from analysis.coref_resolver import resolve_coreferences
from analysis.graph_builder import build_relationship_graph
from fastapi import FastAPI, UploadFile
from ingestion.text_extractor import extract_text
from analysis.classifier import classify_document
from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from nlp.nl_query_handler import answer_nl_query
from monitoring.prometheus_metrics import setup_metrics


app = FastAPI()
setup_metrics(app)

def require_role(required_roles: list[str]):
    def wrapper(Authorize: AuthJWT = Depends()):
        Authorize.jwt_required()
        user = Authorize.get_raw_jwt()
        role = user.get("role", "user")
        if role not in required_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")
    return wrapper
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


@app.post("/relationships/")
async def extract_relationships_api(file: UploadFile):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)
    relationships = extract_relationships(text)

    return {"relationships": relationships[:15]}  # first 15 relationships


@app.post("/graph/")
async def graph_relationships(file: UploadFile):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    raw_text = extract_text(path)
    resolved_text = resolve_coreferences(raw_text)
    triples = extract_relationships(resolved_text)
    html_path = build_relationship_graph(triples)

    return {
        "message": "Graph generated",
        "triples": triples[:10],
        "graph_path": html_path
    }


@app.post("/classify/",dependencies=[Depends(require_role(["admin", "analyst"]))])
async def classify_file(file: UploadFile):
    # Save uploaded file temporarily
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text & classify
    text = extract_text(file_path)
    classification = classify_document(text)

    return {
        "predicted_type": classification["predicted_label"],
        "confidence": classification["confidence"],
        "label_scores": classification["label_scores"]
    }

@app.post("/classify-query/")
async def classify_via_query(file: UploadFile, query: str):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)
    answer = answer_nl_query(text, query)
    return {"answer": answer}