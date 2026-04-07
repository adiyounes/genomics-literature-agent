import anthropic
from config import cfg
from memory.state import AgentState
from rag.retriever import retrieve

client = anthropic.Anthropic(api_key=cfg.anthropic_api_key)

def synthesise(state: AgentState) -> str:
    if not state.chunks:
        return "no evidence collected"
    
    relevant_chunks = retrieve(
        question = state.query,
        chunks = state.chunks,
        chunk_embeddings = state.chunk_embeddings,
        top = 10
    )

    evidence = "\n\n".join(relevant_chunks)

    prompt = f"""

YOU ARE A BIOMEDICAL RESEARCH ASSISTANT

QUERY:
{state.query}

EVIDENCE:
{evidence}

base on the evidence, give a stractured research summary with :

1- Main findings relevant to the query
2- Confidence level and why (high, mid, low)
3- Contradicting evidence if there are any
4- Hypotheses
5- Suggest follow up questions
6- Be concise and say which findings are well supported and which are speculative
"""
    
    responese = client.messages.create(
        model=cfg.model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    return responese.content[0].text