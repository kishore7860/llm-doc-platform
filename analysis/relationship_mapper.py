import spacy
from typing import List, Tuple

nlp = spacy.load("en_core_web_sm")

def extract_relationships(text: str) -> List[Tuple[str, str, str]]:
    doc = nlp(text)
    triples = []

    for sent in doc.sents:
        subject = ""
        obj = ""
        verb = ""

        for token in sent:
            # Subject
            if "subj" in token.dep_:
                subject = token.text

            # Verb (Predicate)
            if token.pos_ == "VERB":
                verb = token.lemma_

            # Object
            if "obj" in token.dep_:
                obj = token.text

        if subject and verb and obj:
            triples.append((subject, verb, obj))

    return triples