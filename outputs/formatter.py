"""
    Formatter
        takes a string from the reasoner and stractures it into a final output
"""

import json
import networkx as nx
from memory.state import AgentState
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich import box

console =Console()

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
    console.print()
    console.print(Panel.fit(
        f"[bold]Query:[/bold] {output['query']}\n"
        f"[dim]Papers read: {output['papers_read']}[/dim]",
        title ="[bold purple]Genomic Literature Mining Agent[/bold purple]",
        border_style="purple", 
    ))

    console.print("\n[bold]Research Summary[/bold]\n")
    console.print(Markdown(output["summary"]))

    if output["gene_connections"]:
        console.print("\n[bold]Gene Co-occurrence Network[/bold]\n")
        table = Table(box=box.SIMPLE, header_style="bold purple")
        table.add_column("Gene A")
        table.add_column("Gene B")
        table.add_column("Co-occurrences", justify="right")
        for conn in output["gene_connections"]:
            table.add_row(
                conn["gene_a"],
                conn["gene_b"],
                str(conn["co_occurrences"])
            )
        console.print(table)

    if output["top_papers"]:
        console.print("\n[bold]Papers Cited[/bold]\n")
        table = Table(box=box.SIMPLE, header_style="bold purple")
        table.add_column("Year", style="dim")
        table.add_column("Title")
        table.add_column("PMID", style="dim")
        for p in output["top_papers"]:
            table.add_row(p["year"],p["title"], p["pmid"])
        console.print(table)