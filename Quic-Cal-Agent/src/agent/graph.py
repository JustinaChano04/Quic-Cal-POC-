from __future__ import annotations
import asyncio

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

# Create server parameters for stdio connection
# from mcp.client.stdio import stdio_client


import asyncio

# """LangGraph single-node graph template.

# Returns a predefined response. Replace logic and configuration as needed.
# """

from dataclasses import dataclass
from typing import Any, Dict, TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

class InputState(TypedDict):
    user_input: str
class OutputState(TypedDict):
    graph_output: str


client = MultiServerMCPClient(
    {
        "Date": {
            "url": "http://date-server:4201/mcp",
            "transport": "streamable_http",
        },
        "Calendar": {   
            "url": "http://calendar-server:4200/mcp",
            "transport": "streamable_http",
        }
    }
)
graph = (StateGraph(InputState, OutputState))

async def get_tool():
    tools = await client.get_tools()
    return tools

tools = asyncio.run(get_tool())
agent = create_react_agent("openai:gpt-4.1", tools)

async def llm_call(state: InputState):
    print(f"Incoming messages: {state}")
    response = await agent.ainvoke({"messages": state["user_input"]})
    return {"response": response}


graph.add_node("llm_call", llm_call)
graph.add_edge("__start__", "llm_call")
compiled = graph.compile(name="New Graph")
print(compiled.config_specs)

