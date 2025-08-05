from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from pydantic import BaseModel
import os

class SlackResult(BaseModel):
    status: str
    channel: str
    message: str

class SlackNotifier:
    """
    A reusable Slack notifier utility.
    """

    def __init__(self, token: str, channel: str = "#hiring"):
        self.client = WebClient(token=token, timeout=60)
        self.channel = channel

    def send_message(self, message: str) -> SlackResult:
        try:
            self.client.chat_postMessage(channel=self.channel, text=message)
            return SlackResult(status="sent", channel=self.channel, message=message)
        except SlackApiError as e:
            return SlackResult(
                status=f"failed: {e.response['error']}",
                channel=self.channel,
                message=message,
            )
