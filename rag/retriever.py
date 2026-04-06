"""
    retriever
        finding the most relevant chunks
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rag.embedder import embed

def retrieve(question: str,chunks: list[str],chunk_embeddings: np.ndarray, top: int=5)-> list[str]:
    qst_vector = embed([question])#embedding the question to make it comparable with the embedded array of chunks
    scores = cosine_similarity(qst_vector, chunk_embeddings)[0]#returning a list of percentages based on where the two vectors point
    #we get scores forom -1.0 to 1.0 we want the chunks closest to 1.0
    top_indices = scores.argsort()[::-1][:top]#returns an array of indices of top 5
    #argsort() returns array of indoces from smallest to largest values
    #[::-1] reverses the order and [:5] takes only the top 5
    return [chunks[i] for i in top_indices]# returns the top 5 chunks using the indices we got before



