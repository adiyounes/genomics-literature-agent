"""
    agent loop
        run -> act -> observe -> reflect cycle
"""


import json
import anthropic
from config import cfg
from tools.registry import TOOLS
from tools.pubmed import search_pubmed, fetch_abstract

client = anthropic.Anthropic(api_key=cfg.anthropic_api_key)

def run(query: str) -> str:
    messages = [{"role": "user", "content": query}]
    iteration = 0

    while iteration < cfg.max_agent_iterations:
        iteration +=1
        response = client.messages.create(
            model=cfg.model,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )
        
        if response.stop_reason == "end_turn":
            return response.content[0].text
        
        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
            
                if tool_name == "search_pubmed":
                    result = search_pubmed(**tool_input)
                elif tool_name == "fetch_abstract":
                    result = fetch_abstract(**tool_input)
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    }
                )
        if tool_results:
            messages.append({"role": "assistant", "content": response.content})
            messages.append(
                {
                    "role": "user",
                    "content": tool_results
                }
            )
    
    return "Agent reached maximum iterations without final answer"
    