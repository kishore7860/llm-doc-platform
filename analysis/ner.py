import spacy

# Load spaCy's small English model

import coreferee

nlp = spacy.load("en_core_web_trf")
nlp.add_pipe("coreferee")

doc = nlp("Kishore is a student. He wants to build a project.")
print(doc._.coref_chains)
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