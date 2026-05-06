# Genomic Literature Mining Agent
---
[![CI](https://github.com/adiyounes/genomics-literature-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/adiyounes/genomics-literature-agent/actions/workflows/ci.yml)

An autonomous AI agent that takes a gene and a disease as input, mines PubMed and bioRxiv, combines evidence across papers, detects contradictions, and returns a structured research summary with a gene–disease knowledge graph.

Built from scratch in pure Python using the Anthropic API, no agent frameworks.

---

## Why no framework

This agent is built without LangChain, LlamaIndex, or any other framework. Every concept the agent loop, tool calling, RAG, memory are implemented from scratch. The goal was to understand what frameworks abstract away before using them.
---

## What it does

You give it a gene and a disease.
0. input: BRCA1 + breast cancer
1. Searches PubMed and bioRxiv autonomously
2. Fetches and reads the most relevant abstracts
3. Uses RAG to retrieve the most relevant passages from collected abstracts
4. Combines findings across papers
5. Flags contradictions between studies
6. Builds a gene–gene co occurrence graph from what it reads
7. Returns a structured research summary with confidence scores
8. output: structured summary + citations + gene co-occurrence network
---

## How it works

The agent runs a loop, plans, acts, observes and reflects until it has enough evidence to answer
```
User query
│
▼
Planner         decides which tools to call and in what order
│
▼
Tools           search_pubmed · fetch_abstract · search_biorxiv · lookup_gene
│
▼
RAG             chunks abstracts → embeds locally → retrieves relevant passages
│
▼
Memory          tracks seen papers · builds co-occurrence graph
│
▼
Reasoner        synthesises evidence · scores confidence · flags contradictions
│
▼
Output          structured summary · citations · gene network
```

Every tool call is executed concurrently using async, if Claude requests multiple searches at once, they all fire simultaneously.

---

## What I learned building it

- How LLM tool calling works at the API level, JSON schema definitions, tool_use response blocks, tool_result messages
- The agent loop plan → act → observe → reflect, and why messages must alternate correctly
- RAG from scratch chunking, local embeddings with sentence transformers, cosine similarity retrieval
- Async Python with httpx, concurrent HTTP requests, asyncio.gather(), AsyncMock for testing
- Testing async and sync code with pytest and unittest.mock
- Docker, containerising a Python application
- GitHub Actions, automated CI pipeline with a live green badge
- AWS ECS + Fargate, deploying a containerised API to the cloud

---

## Stack

| Component | Library | Notes |
|---|---|---|
| LLM | `anthropic` | Claude API |
| Embeddings | `sentence-transformers` | Runs locally, no external API |
| Graph | `networkx` | Gene co-occurrence network |
| HTTP | `httpx` | Async requests |
| XML parsing | `lxml` | PubMed response parsing |
| Terminal output | `rich` | Formatted output, tables, panels |

---
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
```

## Docker

```bash
docker run --rm -t \
  -e ANTHROPIC_API_KEY=your_key \
  -e ENTREZ_EMAIL=your_email \
  genomic-literature-agent \
  --gene BRCA1 --disease "breast cancer"
```

---

## LIVE API

The agent is deployed on AWS ECS and accessible via:

```bash
# Health check
curl http://34.243.52.170:8000/health

# Run the agent
curl -X POST http://34.243.52.170:8000/analyse \
  -H "Content-Type: application/json" \
  -d '{"gene": "BRCA1", "disease": "breast cancer"}'

# Interactive docs
http://34.243.52.170:8000/docs
```

---

## Project structure
```bash
genomics-literature-agent/
├── agent/
│   ├── loop.py          # Core agent loop
│   └── reasoner.py      # Evidence synthesis
├── tools/
│   ├── pubmed.py        # PubMed E-utilities API
│   ├── biorxiv.py       # bioRxiv API
│   ├── gene_ref.py      # NCBI Gene lookup
│   └── registry.py      # Tool schemas for Claude
├── rag/
│   ├── chunker.py       # Abstract chunking
│   ├── embedder.py      # Local sentence-transformers
│   └── retriever.py     # Cosine similarity retrieval
├── memory/
│   ├── state.py         # Agent state
│   └── graph.py         # Gene co-occurrence graph
├── outputs/
│   └── formatter.py     # Structured output
├── tests/               # 16 passing tests
├── config.py
├── main.py
└── .env.example
```
---

## Part of a larger system

This agent is a part of a genomic analysis pipeline that includes pharmacogenomics, pathogenicity prediction, CRISPR simulation, and microbiome integration.

## License

MIT
