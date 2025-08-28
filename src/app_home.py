"""Publish the App Home view."""

from slack_sdk.web.client import WebClient
import json


def update_home_tab(client: WebClient, event):
    with open("./src/views/app_home.json") as f:
        app_home_view = json.load(f)

    # Publish the app home view
    client.views_publish(
        user_id=event["user"],
        # Home tabs must be enabled in your app configuration
        view=app_home_view,
    )
