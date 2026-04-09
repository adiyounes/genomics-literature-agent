import numpy as np
import pytest
from rag.chunker import chunk_text
from rag.embedder import embed
from rag.retriever import retrieve


def test_chunk_text_basic():
    text = "word " * 200
    chunks = chunk_text(text,chunk_size=100, overlap=20)
    assert len(chunks) > 0

def test_chunk_text_overlap():
    text = "word " * 200
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) > 2

def test_chunk_text_short_input():
    text = "too short"
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert chunks == []

def test_chunk_text_chunk_size():
    text = "word " * 200
    chunks = chunk_text(text, chunk_size=50, overlap=10)
    for chunk in chunks:
        assert len(chunk.split()) <= 50

def test_embed_returns_correct_shape():
    chunks = ["BRCA1 repairs DNA damage", "TP53 suppresses tumors"]
    embeddings = embed(chunks)
    assert embeddings.shape == (2, 384)

def test_embed_single_chunk():
    embeddings = embed(["single chunk"])
    assert embeddings.shape == (1, 384)

def test_retrieve_returns_top_k():
    chunks = [
        "BRCA1 repairs DNA damage",
        "TP53 suppresses tumor growth",
        "The weather in Paris is nice",
        "MDM2 regulates TP53",
        "BRCA1 interacts with CHEK2",
    ]
    embeddings = embed(chunks)
    results = retrieve("DNA repair", chunks, embeddings, top = 2)
    assert len(results) == 2

def test_retrieve_relevance():
    chunks = [
        "BRCA1 repairs DNA damage and maintains genomic stability",
        "The weather in Paris is nice today",
    ]
    embeddings = embed(chunks)
    results = retrieve("DNA repair", chunks, embeddings, top = 1)
    assert "BRCA1" in results[0]
