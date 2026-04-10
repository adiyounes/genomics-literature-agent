# Genomic Literature Mining Agent
[![CI](https://github.com/adiyounes/genomics-literature-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/adiyounes/genomics-literature-agent/actions/workflows/ci.yml)

An autonomous AI agent that takes a gene, disease, or variant as input and independently mines PubMed and bioRxiv, synthesises evidence across papers, detects contradictions, and outputs a structured research summary with a gene disease knowledge graph

Built from scratch in pure Python

IMPORTANT: NO AGENT FRAMEWORK USED TO ENSURE I FULLY GRASP THE MECHANICS OF LLM ORCHESTRATION. IMPLEMENTING THE ReAct PATTERN, RAG AND MEMORY MANAGMENT MYSELF, THIS HAS ALLOWED ME TO UNDERSTAND EXACTLY HOW THE ANTHROPIC API HANDLES MULTI STEP REASONING. THIS FOUNDATION ENSURES THAT WHEN I EVENTUALLY MOVE TO A FRAMEWORK, I UNDERSTAND WHAT IS HAPPENING UNDER THE HOOD AND CAN TROUBLESHOOT COMPLEX FAILURES

---

## What it does

Given a query like `BRCA1 breast cancer` or `rs1799966`, the agent:

- Searches PubMed and bioRxiv autonomously
- Fetches and reads relevant abstracts
- Retrieves the most relevant passages using RAG
- Synthesises findings with confidence scores
- Flags contradicting evidence between studies
- Builds a gene–gene and gene–disease co-occurrence graph
- Outputs a structured research summary with citations

## Why no framework

This agent is intentionally built without LangChain, LlamaIndex, or any other agent framework. Every concept, the agent loop, tool calling, RAG, memory is implemented from scratch. My goal is to understand what frameworks abstract away, not to hide behind them

## Architecture

```
User query
     │
     ▼
 Planner        breaks query into subtasks, decides tool order
     │
     ▼
 Tools           search_pubmed · fetch_abstract · gene_cross_ref
     │
     ▼
 Observer + RAG  chunk → embed → retrieve relevant passages
     │
     ▼
 Reasoner        synthesise evidence, score confidence, detect contradictions
     │
     ▼
 Memory          conversation state · seen papers · co-occurrence graph
     │
     ▼
 Output          structured summary · citations · hypotheses · graph
```

## Core concepts

| Concept | Where |
|---|---|
| Agent loop (plan → act → observe → reflect) | `agent/loop.py` |
| Tool use / function calling | `tools/registry.py` |
| RAG (chunk, embed, retrieve) | `rag/` |
| Memory and state management | `memory/state.py` |
| Gene co-occurrence graph | `memory/graph.py` |
| Structured output | `outputs/formatter.py` |

## Quickstart

```bash
# 1. Clone
git clone git@github.com:adiyounes/genomics-literature-agent.git
cd genomics-literature-agent

# 2. Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
# Add your ANTHROPIC_API_KEY and ENTREZ_EMAIL to .env

# 5. Run
python main.py --gene BRCA1 --disease "breast cancer"
python main.py --query "TP53 lung cancer apoptosis"
python main.py --variant rs1799966
```

## Project structure

```
genomics-literature-agent/
├── agent/
│   ├── loop.py          # Core agent loop
│   ├── planner.py       # Query decomposition
│   └── reasoner.py      # Evidence synthesis
├── tools/
│   ├── pubmed.py        # PubMed E-utilities API
│   ├── biorxiv.py       # bioRxiv API
│   ├── gene_ref.py      # NCBI Gene / UniProt
│   └── registry.py      # Tool schemas for Claude
├── rag/
│   ├── chunker.py       # Abstract chunking
│   ├── embedder.py      # Local sentence-transformers
│   └── retriever.py     # Cosine similarity retrieval
├── memory/
│   ├── state.py         # Agent state
│   └── graph.py         # Co-occurrence graph
├── outputs/
│   └── formatter.py     # Structured output
├── tests/
├── config.py
├── main.py
└── .env.example
```

## Stack

- **LLM** — Claude via the Anthropic API
- **Embeddings** — `sentence-transformers` (runs locally, no external API)
- **Graph** — `networkx`
- **HTTP** — `requests` / `httpx`
- **XML parsing** — `lxml`
- **Terminal output** — `rich`

## Part of a larger system

This agent is a component of a unified genomic analysis pipeline that includes pharmacogenomics, pathogenicity prediction, CRISPR simulation, and microbiome integration.

## License

MIT
