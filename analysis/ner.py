import spacy

# Load spaCy's small English model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start_char": ent.start_char,
            "end_char": ent.end_char
        })
    return entities