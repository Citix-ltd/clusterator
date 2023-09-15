import numpy as np
from embedder import Embeddings



def find_close(name: str, embeddings: Embeddings) -> list[tuple[str, float]]:
    """
    finds the top_k closest images to the given name
    returns a list of tuples (name, score), sorted by score
    """
    names = embeddings.names
    vectors = embeddings.vectors
    idx = names.index(name)
    scores = np.dot(vectors, vectors[idx])
    result = [(names[i], scores[i]) for i in range(len(names)) if i != idx]
    sort = sorted(result, key=lambda x: x[1], reverse=True)
    return sort


def merge_close(request: set[str], candidates: list[list[tuple[str, float]]]) -> list[tuple[str, float]]:
    """
    removes duplicates from the list of candidates
    returns a list of tuples (name, score), sorted by score
    """
    candidates = sum(candidates, [])
    merged: dict[str, float] = {}
    for candidate in candidates:
        name, score = candidate
        if name in request:
            continue
        if name in merged:
            merged[name] = max(merged[name], score)
        else:
            merged[name] = score
    sort = sorted(list(merged.items()), key=lambda x: x[1], reverse=True)
    return sort


def find_close_to_many(names: set[str], embeddings: Embeddings) -> list[tuple[str, float]]:
    """
    finds the top_k closest images to the given list of names
    returns a list of tuples (name, score), sorted by score
    """
    candidates = [find_close(name, embeddings) for name in names]
    return merge_close(names, candidates)


