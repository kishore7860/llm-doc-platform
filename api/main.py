from ingestion.text_extractor import extract_text
from ingestion.metadata_extractor import extract_basic_metadata
from rag.retriever import chunk_document, build_vector_index, query_vector_index
from analysis.ner import extract_entities
from analysis.summarizer import summarize
from analysis.relationship_mapper import extract_relationships
from analysis.coref_resolver import resolve_coreferences
from analysis.graph_builder import build_relationship_graph
from fastapi import FastAPI, UploadFile ,Form
from ingestion.text_extractor import extract_text
from analysis.classifier import classify_document
from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from nlp.nl_query_handler import answer_nl_query
from fastapi.middleware.cors import CORSMiddleware
from monitoring.prometheus_metrics import setup_metrics
from auth import auth
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi

app = FastAPI()
security = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="LLM Document Processing API",
        version="1.0.0",
        description="Secure document classification, summarization, entity extraction, and relationship mapping.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "security" not in openapi_schema["paths"][path][method]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
setup_metrics(app)

def require_role(required_roles: list[str]):
    def wrapper(Authorize: AuthJWT = Depends()):
        Authorize.jwt_required()
        user = Authorize.get_raw_jwt()
        role = user.get("role", "user")
        if role not in required_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")
    return wrapper

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), Authorize: AuthJWT = Depends()):
    try:
        if username == "admin" and password == "admin":
            access_token = Authorize.create_access_token(
                subject=username, user_claims={"role": "admin"}
            )
            return {"access_token": access_token}
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

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


@app.post("/classify/", dependencies=[Depends(require_role(["admin", "analyst"]))])
async def classify_file(file: UploadFile):
    try:
        print(f"✅ Received file: {file.filename}")
        
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            print(f"📦 Writing file to disk: {file_path} ({len(content)} bytes)")
            f.write(content)

        # Extract text
        text = extract_text(file_path)
        print(f"📝 Extracted text (first 300 chars):\n{text[:300]}\n")

        if not text.strip():
            raise ValueError("❌ No text extracted from document!")

        # Run classification
        classification = classify_document(text)
        print("🎯 Classification result:", classification)

        return {
            "predicted_type": classification["predicted_label"],
            "confidence": classification["confidence"],
            "label_scores": classification["label_scores"]
        }

    except Exception as e:
        import traceback
        print("🚨 ERROR during classification:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/classify-query/")
async def classify_via_query(file: UploadFile, query: str):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)
    answer = answer_nl_query(text, query)
    return {"answer": answer}