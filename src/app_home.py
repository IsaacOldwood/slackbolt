"""Publish the App Home view."""

from slack_sdk.web.client import WebClient
import json


def update_home_tab(client: WebClient, event):
    with open("./src/views/app_home.json") as f:
        app_home_view = json.load(f)

    # Call views.publish with the built-in client
    client.views_publish(
        # Use the user ID associated with the event
        user_id=event["user"],
        # Home tabs must be enabled in your app configuration
        view=app_home_view,
    )
