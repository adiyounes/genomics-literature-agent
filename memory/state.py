"""
    Agent state:
        tracking everything the agent knows across iterations
"""
from dataclasses import dataclass, field
import numpy as np

@dataclass
class AgentState:
    query: str = ""
    seen_pmids: set = field(default_factory=set)
    abstracts: list[dict] = field(default_factory=list)
    chunks: list[str] = field(default_factory=list)
    chunk_embeddings: np.ndarray = field(default_factory=lambda: np.empty((0, 384)))
    hypotheses: list[str] = field(default_factory=list)
    
