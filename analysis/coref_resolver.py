import spacy
import coreferee

nlp = spacy.load("en_core_web_trf")
# Add the coreferee pipe (this must be added AFTER loading the model)
if not nlp.has_pipe("coreferee"):
    nlp.add_pipe("coreferee")

def resolve_coreferences(text: str) -> str:
    doc = nlp(text)
    if hasattr(doc._, "resolved_text"):
        return doc._.resolved_text
    else:
        return text  # fallback if coreference fails