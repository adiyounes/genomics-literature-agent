"""
    FastAPI wrapper
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.loop import run


app = FastAPI(
    title = "Genomic Literature Mining Agent",
    description = "Literature mining for genomics research",
    version="0.1.0",
)



class AnalyseRequest(BaseModel):
    gene: str = ""
    disease: str = ""
    query: str = ""

class AnalyseResponse(BaseModel):
    query: str
    summary: str
    papers_read: int
    top_papers: list
    gene_connections: list

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyse", response_model=AnalyseResponse)
async def analyse(request: AnalyseRequest):
    if not request.query and not request.gene:
        raise HTTPException(
            status_code=400,
            detail="Provide either 'query' or 'gene' in request body"
        )
    
    if request.query:
        query = request.query
    else:
        parts = [request.gene]
        if request.disease:
            parts.append(request.disease)
        query = " ".join(parts)

    result = await run (query)
    return result