#!/usr/bin/env python

import asyncio
import websockets
import os
import json
from agent import query

from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools

import asyncio


# establishing mcp clients and connection to servers
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
# 
# date_server_params = StdioServerParameters(
#     command="python",
#     args=["/Users/justinchan/Desktop/repos/mcp_agent/date_server.py"],
# )
# gcal_server_params = StdioServerParameters(
#     command="python",
#     args=["/Users/justinchan/Desktop/repos/mcp_agent/gcal_server.py"],
# )


async def llm_call(message):

    tools = await client.get_tools()
    print(tools)
    agent = create_react_agent("openai:gpt-4.1", tools)
    print(message)
    response = await agent.ainvoke({"messages": message})

    import json
    from langchain.load.dump import dumpd
    json_string = dumpd(response)
    with open("output.json", "w") as fp:
        json.dump(json_string, fp)
    return json_string

async def echo(websocket):  
    try:
        async for message in websocket:
            print("Received message:", message, flush=True)
            llm_results = await llm_call(message)
            # Echo the message back
            await websocket.send(f'{llm_results}')
            await websocket.send("[END]")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)

async def main():
    print("WebSocket server starting", flush=True)
    
    # Create the server with CORS headers
    async with websockets.serve(
        echo,
        "0.0.0.0",
        int(os.environ.get('PORT', 8092))
    ) as server:
        print("WebSocket server running on port 8091", flush=True)
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(llm_call('hi'))