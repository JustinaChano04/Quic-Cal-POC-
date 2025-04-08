from ollama import chat
import re
import httpx
import json

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        result = chat("phi4", messages=self.messages)
        message = result["message"]["content"]
        return message


class AssistantBot:
    def __init__(self, system=""):
        from openai import OpenAI
        with open("secrets.json") as file:
            assistant_id = json.load(file)["secrets"]["assistant_id"]
            
        self.client = OpenAI()
        self.thread = self.client.beta.threads.create()
        self.assistant = self.client.beta.assistants.retrieve(
            assistant_id
        )

    def __call__(self, message):
        result = self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=message
        )
        result = self.execute(message)
        return result

    def execute(self, message):
        from typing_extensions import override
        from openai import AssistantEventHandler

        # First, we create a EventHandler class to define
        # how we want to handle the events in the response stream.

        class EventHandler(AssistantEventHandler):
            def __init__(self):
                super().__init__()
                self.response_text = (
                    ""  # Initialize an empty string to store the response
                )

            @override
            def on_text_created(self, text) -> None:
                print(f"\nassistant > ", end="", flush=True)

            @override
            def on_text_delta(self, delta, snapshot):
                print(delta.value, end="", flush=True)
                self.response_text += (
                    delta.value
                )  # Append streamed text to response_text

            def on_tool_call_created(self, tool_call):
                print(f"\nassistant > {tool_call.type}\n", flush=True)

        handler = EventHandler()
        with self.client.beta.threads.runs.stream(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            event_handler=handler,
        ) as stream:
            stream.until_done()
        return handler.response_text


# ACTIONS
def wikipedia(q):
    return httpx.get(
        "https://en.wikipedia.org/w/api.php",
        params={"action": "query", "list": "search", "srsearch": q, "format": "json"},
    ).json()["query"]["search"][0]["snippet"]


def calculate(what):
    return eval(what)


def create_event(event_info):
    event_info = event_info.replace(" ", "")
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    print("create_event called", event_info.replace(" ", ""))
    event_name, date, start_time, end_time = event_info.split(",")
    print("log", event_name, date, start_time, end_time)

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
    try:
        event = {
            "summary": f"{event_name}",
            "start": {
                "dateTime": f"{date}T{start_time}-05:00",
            },
            "end": {
                "dateTime": f"{date}T{end_time}-05:00",
            },
        }
        service = build("calendar", "v3", credentials=creds)
        event = service.events().insert(calendarId="primary", sendUpdates="all", body=event).execute()
        return event_info.split(",")
    except HttpError as error:
        print(f"An error occurred: {error}")


def find_date(date):
    from datetime import date

    print("find_date", date.today())
    return date.today()


# QUERY
def query(next_prompt, max_turns=5):
    known_actions = {
        "wikipedia": wikipedia,
        "create_calendar": create_event,
        "find_date": find_date,
    }
    action_re = re.compile("^Action: (\w+): (.*)$")

    bot = AssistantBot()
    for i in range(max_turns):
        stream = bot(next_prompt)

        actions = [action_re.match(a) for a in stream.split("\n") if action_re.match(a)]
        if not actions:
            break  # we're done
        print("action log: ", actions)
        # an action to run
        action, action_input = actions[0].groups()
        if action not in known_actions:
            raise Exception("Unknown action: {}: {}".format(action, action_input))
        print(" -- running {} {}".format(action, action_input))
        observation = known_actions[action](action_input)
        print("Observation:", observation)
        next_prompt = "Observation: {}".format(observation)

    return stream, observation, next_prompt


if __name__ == "__main__":
    from datetime import date
    query("FPAS Discussion for Feb 18th 2025, from 1:00pm to 2:00pm")
