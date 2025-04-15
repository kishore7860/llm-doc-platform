from transformers import pipeline

# Load Hugging Face summarization pipeline (bart-based)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")
def summarize(text: str, max_length: int = 180, min_length: int = 60):
    if len(text.split()) < 50:
        return text  # skip summarizing short text
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]["summary_text"]