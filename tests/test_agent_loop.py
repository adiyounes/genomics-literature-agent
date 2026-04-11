import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from agent.loop import run

@pytest.mark.asyncio
async def test_loop_returns_string_output():
    with patch("agent.loop.client") as mock_client:
        mock_response = MagicMock()
        mock_response.stop_reason = "end_turn"
        mock_response.content = [MagicMock(type="text", text="BRCA1 is a tumor suppressor.")]
        mock_client.messages.create.return_value = mock_response

        result = await run("BRCA1 breast cancer")

        assert isinstance(result, dict)
        assert "summary" in result
        assert "query" in result

@pytest.mark.asyncio
async def test_loop_handles_tool_call():
    with patch("agent.loop.client") as mock_client, \
         patch("agent.loop.search_pubmed", new_callable=AsyncMock) as mock_search, \
         patch("agent.loop.fetch_abstract", new_callable=AsyncMock) as mock_fetch:

        mock_search.return_value = ["12345"]
        mock_fetch.return_value = {
            "pmid": "12345",
            "title": "BRCA1 and DNA repair",
            "abstract": "BRCA1 repairs DNA damage in breast cancer cells.",
            "authors": ["Smith J"],
            "year": "2023",
        }

        tool_response = MagicMock()
        tool_response.stop_reason = "tool_use"
        tool_block = MagicMock()
        tool_block.type = "tool_use"
        tool_block.id = "toolu_1"
        tool_block.name = "search_pubmed"
        tool_block.input = {"query": "BRCA1 breast cancer"}
        
        tool_response.content = [tool_block]

        final_response = MagicMock()
        final_response.stop_reason = "end_turn"
        final_response.content = [MagicMock(type="text", text="BRCA1 is a tumor suppressor.")]

        mock_client.messages.create.side_effect = [tool_response, final_response]

        result = await run("BRCA1 breast cancer")

        assert isinstance(result, dict)
        mock_search.assert_called_once()