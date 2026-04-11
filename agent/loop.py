"""
    agent loop
        run -> act -> observe -> reflect cycle
"""


import json
import asyncio
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
from tools.biorxiv import search_biorxiv
from tools.gene_ref import lookup_gene

console = Console(force_terminal=True)

client = anthropic.Anthropic(api_key=cfg.anthropic_api_key)

async def execute_tool(tool_name: str, tool_input: dict) -> any:
    if tool_name == "search_pubmed":
        with console.status(f"[dim]Searching PubMed for '{tool_input.get('query')}'...[/dim]"):
            return await search_pubmed(**tool_input)
    elif tool_name == "fetch_abstract":
        with console.status(f"[dim]Fetching abstract {tool_input.get('pmid')}...[/dim]"):
            return await fetch_abstract(**tool_input)
    elif tool_name == "search_biorxiv":
        with console.status(f"[dim]Searching bioRxiv for '{tool_input.get('query')}'...[/dim]"):
            return await search_biorxiv(**tool_input)
    elif tool_name == "lookup_gene":
        with console.status(f"[dim]Looking up gene {tool_input.get('symbol')}...[/dim]"):
            return await lookup_gene(**tool_input)
    else:
        return {"error": f"Unknown tool: {tool_name}"}

async def run(query: str) -> dict:

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
        
        tool_blocks = [b for b in response.content if b.type == "tool_use"]
        
        if tool_blocks:
            results = await asyncio.gather(
                *[
                    execute_tool(b.name,b.input) for b in tool_blocks
                ]
            )
        
            for block, result in zip(tool_blocks, results):
                if block.name == "fetch_abstract" and result and result["pmid"] not in state.seen_pmids:
                    state.seen_pmids.add(result["pmid"])
                    state.abstracts.append(result)
                    new_chunks = chunk_text(result["abstract"])
                    new_embeddings = embed(new_chunks)
                    state.chunks.extend(new_chunks)
                    if new_embeddings.size > 0:
                        state.chunk_embeddings = np.vstack(
                            [state.chunk_embeddings, new_embeddings]
                        )
                    graph = update_graph(graph, result["abstract"])
            
            tool_results = [
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result)
                }
                for block, result in zip(tool_blocks, results)
            ]

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        

        
    summary = synthesise(state)
    return format_output(summary, state, graph)
    