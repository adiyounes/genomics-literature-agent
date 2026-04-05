"""
    Tool regestry:
        describing the avaliable tools to Claude
"""

TOOLS = [
    {
        "name": "search_pubmed",
        "description": (
            "Search PubMed for biomedical literature"
            "Use this when you need abstracts about gene, desease or variant"
            "Returns a list of paper IDs (PMIDs)"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query":{
                    "type": "string",
                    "description":"Search query e.g. 'BRCA1 breast cancer apoptosis'"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Number of results to return. default 10, max 20"
                },
            },
            "required":["query"]
        },
    },
    {
        "name":"fetch_abstract",
        "description":(
            "fetch the full abstract and metadata for PubMed paper by its PMID"
            "always call this after search_pubmed to get the actual content"
        ),
        "input_schema":{
            "type": "object",
            "properties":{
                "pmid": {
                    "type": "string",
                    "description": "PubMed ID of the paper e.g. '153264'"
                },
            },
            "required": ["pmid"]
        },
   },
]