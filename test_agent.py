#!/usr/bin/env python

import asyncio
import websockets
import os
import json
from agent import query


async def echo(websocket):  
    try:
        async for message in websocket:
            print("Received message:", message, flush=True)
            result, observation, next_prompt = query(message) 
            # Echo the message back
            await websocket.send(f'{result} \n {observation} \n {next_prompt}')
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
        int(os.environ.get('PORT', 8090))
    ) as server:
        print("WebSocket server running on port 8090", flush=True)
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())