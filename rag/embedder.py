"""
    Embedder
        converting chunks of text into vectors
"""

from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")#this model reads a text and outputs a list of 384 numbers that represent it's meaning

def embed(texts: list[str]) -> np.ndarray:
    return model.encode(texts, convert_to_numpy=True)#text -> 2d numpy array