from __future__ import annotations
import asyncio
import websockets
import os
import json
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools

import asyncio

# """LangGraph single-node graph template.

# Returns a predefined response. Replace logic and configuration as needed.
# """



from dataclasses import dataclass
from typing import Any, Dict, TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

class Configuration(TypedDict):
    """Configurable parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
    """

    my_configurable_param: str

@dataclass
class State(TypedDict):
    messages: Annotated[list, add_messages]


# async def call_model(state: State, config: RunnableConfig) -> Dict[str, Any]:
#     """Process input and returns output.

#     Can use runtime configuration to alter behavior.
#     """
#     configuration = config["configurable"]
#     return {
#         "changeme": "output from call_model. "
#         f'Configured with {configuration.get("my_configurable_param")}'
#     }

client = MultiServerMCPClient(
    {
        "Date": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["/Users/justinchan/Desktop/repos/ReAct-Agent-Experiment/date_server.py"],
            "transport": "stdio",
        },
        "Calendar": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["/Users/justinchan/Desktop/repos/ReAct-Agent-Experiment/gcal_server.py"],
            "transport": "stdio",
        }
    }
)
async def get_tool():
    tools = await client.get_tools()
    return tools
tools = asyncio.run(get_tool())
agent = create_react_agent("openai:gpt-4.1", tools)
# agent = initial()

async def llm_call(state: State):
    # graph = create_react_agent("openai:gpt-4.1", tools)
    response = await agent.ainvoke({"role": "user", "messages": state["messages"]})
    return {"role": "user", "content": response, }

graph = (
    StateGraph(State, config_schema=Configuration)
    .add_node("llm_call", llm_call)
    .add_edge("__start__", "llm_call")
    .compile(name="New Graph")
)
# async def llm_call():
#     tools = await client.get_tools()
#     graph = create_react_agent("openai:gpt-4.1")
#     return graph
#     # response =  agent.ainvoke({"messages": 'message'})

#     # import json
#     # from langchain.load.dump import dumpd
#     # json_string = dumpd(response)
#     # with open("output.json", "w") as fp:
#     #     json.dump(json_string, fp)

# graph = llm_call()
# if __name__ == "__main__":
    # asyncio.run(llm_call("what is today's date?"))