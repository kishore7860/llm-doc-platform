from transformers import pipeline
from typing import List, Dict
from monitoring.mlflow_tracker import log_classification_run


# Initialize zero-shot classifier using BART-MNLI
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define categories your platform will support
CANDIDATE_LABELS = [
    "Contract",
    "Legal Document",
    "Business Report",
    "Technical Specification",
    "Meeting Minutes",
    "Proposal",
    "Financial Statement",
    "Invoice",
    "Policy Document"
]

def classify_document(text: str, labels: List[str] = CANDIDATE_LABELS) -> Dict:
    """
    Classify document text using zero-shot learning.

    Parameters:
        text: Extracted document text
        labels: List of labels to classify against

    Returns:
        dict containing best label and label scores
    """
    result = classifier(text[:1000], candidate_labels=labels)  # Truncate for speed
    return {
        "predicted_label": result["labels"][0],
        "confidence": result["scores"][0],
        "label_scores": dict(zip(result["labels"], result["scores"]))
    }

def classify_document(text: str, labels: List[str] = CANDIDATE_LABELS) -> Dict:
    result = classifier(text[:1000], candidate_labels=labels)
    log_classification_run(
        input_text=text,
        predicted_label=result["labels"][0],
        confidence=result["scores"][0]
    )
    return {
        "predicted_label": result["labels"][0],
        "confidence": result["scores"][0],
        "label_scores": dict(zip(result["labels"], result["scores"]))
    }