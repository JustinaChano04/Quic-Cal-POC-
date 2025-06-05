# from ollama import chat
import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from mcp.server.fastmcp import FastMCP
from datetime import datetime
from zoneinfo import ZoneInfo

from server_helper import g_cal_connect

mcp = FastMCP("Date")

@mcp.tool()
def get_datetime() -> str:
    """Get today's datetime"""
    eastern_time = datetime.now(ZoneInfo("America/New_York"))
    return eastern_time

if __name__ == "__main__":
    mcp.run(transport="stdio")