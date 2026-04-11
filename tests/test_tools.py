import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from tools.registry import TOOLS
from tools.pubmed import search_pubmed, fetch_abstract
from memory.graph import extract_genes, update_graph
import networkx as nx
import pytest


@pytest.mark.asyncio
async def test_search_pubmed_returns_pmids():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "esearchresult": {"idlist": ["12345", "67890"]}
    }

    with patch("tools.pubmed.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
        mock_client.return_value.__aexit__ = AsyncMock(return_value=False)
        
        mock_client.return_value.get = AsyncMock(return_value=mock_response)

        result = await search_pubmed("BRCA1 breast cancer")

        assert result == ["12345","67890"]
        assert len(result) == 2

@pytest.mark.asyncio
async def test_fetch_abstract_return_dict():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.content = b"""
    <PubmedArticleSet>
        <PubmedArticle>
            <ArticleTitle>BRCA1 and DNA repair</ArticleTitle>
            <Abstract>
                <AbstractText>BRCA1 repairs DNA damage.</AbstractText>
            </Abstract>
            <PubDate><Year>2023</Year></PubDate>
        </PubmedArticle>
    </PubmedArticleSet>
    """
    with patch("tools.pubmed.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
        mock_client.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_client.return_value.get = AsyncMock(return_value = mock_response)

        result = await fetch_abstract("12345")
        
        assert result["pmid"] == "12345"
        assert result["title"] == "BRCA1 and DNA repair"
        assert result["year"] == "2023"

def test_extract_genes_finds_gene_symbols():
    genes = extract_genes("BRCA1 and TP53 regulate DNA damage response")
    assert "BRCA1" in genes
    assert "TP53" in genes
    assert "DNA" not in genes

def test_update_graph_creates_edges():
    graph = nx.Graph()
    graph = update_graph(graph, "BRCA1 and TP53 are tumor suppressors")
    assert graph.has_node("BRCA1")
    assert graph.has_node("TP53")
    assert graph.has_edge("BRCA1", "TP53")

def test_registry_has_required_tools():
    tool_names = [t["name"] for t in TOOLS]
    assert "search_pubmed" in tool_names
    assert "fetch_abstract" in tool_names

def test_regestiry_tools_have_required_fields():
    for tool in TOOLS:
        assert "name" in tool
        assert "description" in tool
        assert "input_schema" in tool
        assert tool["input_schema"]["type"] == "object"