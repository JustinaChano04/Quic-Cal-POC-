# from ollama import chat
from datetime import datetime
from fastmcp import FastMCP
from zoneinfo import ZoneInfo


mcp = FastMCP("Date")

@mcp.tool()
def get_datetime() -> str:
    """Get today's datetime"""
    eastern_time = datetime.now(ZoneInfo("America/New_York"))
    return eastern_time

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=4201,host="0.0.0.0", path="/mcp")
