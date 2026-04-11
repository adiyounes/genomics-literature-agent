"""
    NCBI gene database look up
        gene symbol -> official name,summary, organizm and chromosomal location
"""

import httpx
from lxml import etree
from config import cfg
import asyncio


BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

async def search_gene(symbol: str) -> str | None:
    params = {
        "db": "gene",
        "term": f"{symbol}[sym] AND human[organism]",
        "retmax": 1,
        "retmode": "xml",
        "email": cfg.entrez_email,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/esearch.fcgi",
            params = params,
            timeout = 10,
        )
    response.raise_for_status()
    await asyncio.sleep(0.34)

    data = etree.fromstring(response.content)
    ids = data.findall(".//Id")
    return ids[0].text if ids else None

async def fetch_gene_info(gene_id: str) -> dict | None:
    params ={
        "db": "gene",
        "id": gene_id,
        "retmode": "xml",
        "email": cfg.entrez_email,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/efetch.fcgi",
                params = params,
                timeout = 10
            )
        response.raise_for_status()
        await asyncio.sleep(0.34)
        
        root = etree.fromstring(response.content)

        name = root.findtext(".//Gene-ref_locus") or ""
        fullname = root.findtext(".//Gene-ref_desc") or ""
        summary = root.findtext(".//Entrezgene_summary") or ""
        chromosome = root.findtext(".//SubSource_name") or ""


        return {
            "gene_id": gene_id,
            "symbol": name,
            "full_name": fullname,
            "summary": summary,
            "chromosome": chromosome,
        }
    
    except httpx.HTTPStatusError as e:
        print(f"Error fetching gene {gene_id}: {e}")
        return None
    
async def lookup_gene(symbol: str) -> dict | None:
    gene_id = await search_gene(symbol)
    if gene_id is not None:
        return await fetch_gene_info(gene_id)
    else:
        return None