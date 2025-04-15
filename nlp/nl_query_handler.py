from analysis.classifier import classify_document
from ingestion.text_extractor import extract_text

def answer_nl_query(text: str, query: str) -> str:
    classification = classify_document(text)
    label = classification["predicted_label"]
    
    if "type" in query or "kind" in query:
        return f"This document appears to be a **{label}** (Confidence: {classification['confidence']:.2f})."
    elif "is this a contract" in query.lower():
        if label == "Contract":
            return f"Yes, it is classified as a contract with confidence {classification['confidence']:.2f}."
        else:
            return f"No, it appears to be a {label}."
    else:
        return f"I classified this document as a **{label}**. You may refine the question further for better context."