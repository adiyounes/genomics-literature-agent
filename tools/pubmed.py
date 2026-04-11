"""
    PubMed API wrapper

    functions:
        search_pubmed query-> list fo PMIDs
        fetch_abstract PMID -> title, abstract, authors, year
"""


import time
import requests
from lxml import etree
from config import cfg


BASE_URL="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def search_pubmed(query: str, max_results: int = 10,) -> list[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "email": cfg.entrez_email,    
    }

    response = requests.get(f"{BASE_URL}/esearch.fcgi", params=params)
    response.raise_for_status()
    time.sleep(0.34)

    data = response.json()
    return data["esearchresult"]["idlist"]

def fetch_abstract(pmid: str) -> dict:
    try:
        params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml", #the format i want
        "rettype": "abstract", #the type of content i want just the abstract not the whole document
        "email": cfg.entrez_email,
        }

        response = requests.get(f"{BASE_URL}/efetch.fcgi", params=params, timeout=10)
        response.raise_for_status()
        time.sleep(0.34)

        root = etree.fromstring(response.content)

        if root.find(".//ArticleTitle") is None:
            return None
        
        title = root.findtext(".//ArticleTitle") or ""
        abstract = root.findtext(".//AbstractText") or ""
        year = root.findtext(".//PubDate/Year") or ""
        authors = [
            f"{a.findtext('LastName')} {a.findtext('ForName')}"
            for a in root.findall(".//Author")
            if a.findtext("LastName")
        ]

        return {
            "pmid": pmid,
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "year": year,
        }
    except requests.exceptions.Timeout:
        print(f"Timeout fetching PMID {pmid}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching PMID {pmid}: {e}")
        return None