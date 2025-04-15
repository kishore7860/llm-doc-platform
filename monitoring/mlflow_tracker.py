import mlflow
from datetime import datetime

def log_classification_run(input_text: str, predicted_label: str, confidence: float, model_name: str = "bart-mnli"):
    mlflow.set_tracking_uri("http://localhost:5000")  # Default tracking server
    mlflow.set_experiment("document_classification")

    with mlflow.start_run(run_name=f"classify-{datetime.now().isoformat()}"):
        mlflow.log_param("model", model_name)
        mlflow.log_param("input_length", len(input_text))
        mlflow.log_metric("confidence", confidence)
        mlflow.log_metric("prediction_length", len(predicted_label))
        mlflow.log_text(input_text[:500], "input_preview.txt")
        mlflow.log_text(predicted_label, "prediction.txt")