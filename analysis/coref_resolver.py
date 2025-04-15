import spacy
import coreferee

nlp = spacy.load("en_core_web_trf")
nlp.add_pipe("coreferee")

def resolve_coreferences(text: str) -> str:
    doc = nlp(text)
    return doc._.resolved_text
