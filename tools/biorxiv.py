"""
    bioRxiv Api Wrapper
        topic ->  title, abstract, authors, DOI
"""


import httpx
from datetime import datetime, timedelta 
import asyncio
BASE_URL = "https://api.biorxiv.org"

async def search_biorxiv(query: str, max_results: int = 10) -> list[dict]:
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/details/biorxiv/{start_date}/{end_date}/0/json",
            timeout = 30,
        )

    response.raise_for_status()
    await asyncio.sleep(0.5)

    data = response.json()
    papers = data.get("collection", [])

    query_lower = query.lower()
    filtered = [
        p for p in papers
        if query_lower in p.get("title", "").lower()
        or query_lower in p.get("abstract", "").lower()
    ]


    return [
        {
            "doi": p.get("doi", ""),
            "title": p.get("title", ""),
            "abstract": p.get("abstract", ""),
            "authors": p.get("authors", ""),
            "date": p.get("date", ""),
            "category": p.get("category", ""),
        }
        for p in papers[:max_results]
    ]