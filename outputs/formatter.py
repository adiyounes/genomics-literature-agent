"""
    Formatter
        takes a string from the reasoner and stractures it into a final output
"""

import json
import networkx as nx
from memory.state import AgentState

def format_output(summary: str, state: AgentState, graph: nx.Graph) -> dict:
    return {
        "query": state.query,
        "summary": summary,
        "papers_read": len(state.abstracts),
        "top_papers": [
            {
                "pmid": p["pmid"],
                "title": p["title"],
                "year": p["year"],
            }
            for p in state.abstracts[:5]
        ],
        "gene_connections": [
            {
                "gene_a": a,
                "gene_b": b,
                "co_occurrences": d["weight"],
            }
            for a,b,d in sorted(
                graph.edges(data=True),
                key= lambda x: x[2]["weight"],
                reverse= True,
            ) [:10]
        ],
    }

def print_output(output: dict) -> None:
    print("\n" + "-" * 60)
    print(f"QUERY: {output['query']}")
    print(f"PAPERS READ: {output['papers_read']}")
    print("-" * 60)
    print("\nRESEARCH SUMMARY:")
    print(output['summary'])
    print("\nTOP GENE CONNECTIONS:")
    for conn in output['gene_connections']:
        print(f" {conn['gene_a']}--{conn['gene_b']} ({conn['co_occurrences']} papers)")
    print("\nPAPERS CITED:")
    for p in output["top_papers"]:
        print(f"[{p['year']}] {p['title']} (PMID: {p['pmid']})")
    print("-" * 60)
    
