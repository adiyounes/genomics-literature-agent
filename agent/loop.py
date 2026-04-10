"""
    agent loop
        run -> act -> observe -> reflect cycle
"""


import json
import anthropic
from config import cfg
import numpy as np
import networkx as nx
from tools.registry import TOOLS
from tools.pubmed import search_pubmed, fetch_abstract
from memory.state import AgentState
from memory.graph import update_graph
from rag.chunker import chunk_text
from rag.embedder import embed
from agent.reasoner import synthesise
from outputs.formatter import format_output
from rich.console import Console

console = Console()

client = anthropic.Anthropic(api_key=cfg.anthropic_api_key)

def run(query: str) -> dict:

    messages = [{"role": "user", "content": query}]
    iteration = 0

    state = AgentState(query=query)
    graph = nx.Graph()

    while iteration < cfg.max_agent_iterations:
        iteration +=1
        with console.status("[dim]Thinking...[/dim]"):
            response = client.messages.create(
                model=cfg.model,
                max_tokens=1024,
                tools=TOOLS,
                messages=messages,
                )
        
        if response.stop_reason == "end_turn":
            summary = synthesise(state)
            return format_output(summary, state, graph)
        
        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
            
                if tool_name == "search_pubmed":
                    with console.status(f"[dim]Searching PubMed for '{tool_input.get('query')}'...[/dim]"):
                        result = search_pubmed(**tool_input)
                elif tool_name == "fetch_abstract":
                    with console.status(f"[dim]Fetching abstract for '{tool_input.get('pmid')}'...[/dim]"):
                        result = fetch_abstract(**tool_input)
                    if result and result["pmid"] not in state.seen_pmids:
                        state.seen_pmids.add(result['pmid'])
                        state.abstracts.append(result)
                        new_chunks = chunk_text(result['abstract'])
                        new_embeddings = embed(new_chunks)
                        state.chunks.extend(new_chunks)
                        if new_embeddings.size > 0:
                            state.chunk_embeddings = np.vstack(
                                [state.chunk_embeddings, new_embeddings]
                                )
                        graph = update_graph(graph, result['abstract'])
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    }
                )
        if tool_results:
            messages.append({"role": "assistant", "content": response.content})
            messages.append(
                {
                    "role": "user",
                    "content": tool_results
                }
            )
    summary = synthesise(state)
    output = format_output(summary, state, graph)
    return output
    