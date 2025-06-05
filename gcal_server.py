# from ollama import chat
import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from mcp.server.fastmcp import FastMCP
from datetime import datetime
from zoneinfo import ZoneInfo

from server_helper import g_cal_connect

mcp = FastMCP("Calendar")

@mcp.tool()
def create_event(event_name: str, date: str, start_time: str, end_time: str):
    return {"name": event_name, "date": date, "start_time": start_time, "end_time": end_time}
    # pass
    # event_info = event_info.replace(" ", "")
    # event_name, date, start_time, end_time = event_info.split(",")
    # # split event info 
    # creds = g_cal_connect()

    # try:
    #     event = {
    #         "summary": f"{event_name}",
    #         "start": {
    #             "dateTime": f"{date}T{start_time}-05:00",
    #         },
    #         "end": {
    #             "dateTime": f"{date}T{end_time}-05:00",
    #         },
    #     }

    #     service = build("calendar", "v3", credentials=creds)
    #     # create event based off of event data from LLM

    #     event = service.events().insert(calendarId="primary", sendUpdates="all", body=event).execute()
    #     return event_info.split(",")
    
    # except HttpError as error:
    #     print(f"An error occurred: {error}")

if __name__ == "__main__":
    mcp.run(transport="stdio")