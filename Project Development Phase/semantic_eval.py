import math
import re
from collections import Counter

_MODEL = None


def _tokenize(text):
    return re.findall(r"\w+", (text or "").lower())


def _counter_cosine(c1, c2):
    dot = sum(v * c2.get(k, 0) for k, v in c1.items())
    norm1 = math.sqrt(sum(v * v for v in c1.values()))
    norm2 = math.sqrt(sum(v * v for v in c2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def _get_sentence_transformer():
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer

        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL


def semantic_similarity(text1, text2):
    try:
        model = _get_sentence_transformer()
        import numpy as np

        emb1 = model.encode([text1])[0]
        emb2 = model.encode([text2])[0]
        dot = float(np.dot(emb1, emb2))
        norm = float(np.linalg.norm(emb1) * np.linalg.norm(emb2) + 1e-8)
        return dot / norm
    except Exception:
        t1 = _tokenize(text1)
        t2 = _tokenize(text2)
        return float(_counter_cosine(Counter(t1), Counter(t2)))
