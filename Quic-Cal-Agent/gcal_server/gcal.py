from fastmcp import FastMCP
mcp = FastMCP("Calendar")

@mcp.tool()
def create_event(event_name: str, date: str, start_time: str, end_time: str):
    return {"message": f"{event_name}, {date}, {start_time}, {end_time}"}
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
    #     return {"event": event}
    
    # except HttpError as error:
    #     print(f"An error occurred: {error}")

if __name__ == "__main__":
    mcp.run(transport="streamable-http",port=4200,host="0.0.0.0", path="/mcp")