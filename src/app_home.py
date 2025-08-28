"""Publish the App Home view."""

from slack_sdk.web.client import WebClient
import json


def initial_home_open(client: WebClient, event):
    with open("./src/app_home.json") as f:
        app_home_view = json.load(f)

    # Publish the app home view
    client.views_publish(
        user_id=event["user"],
        # Home tabs must be enabled in your app configuration
        view=app_home_view,
    )


def stage_2_home_open(ack, client: WebClient, body):
    ack()

    with open("./src/stage_2/views/app_home.json") as f:
        app_home_view = json.load(f)

    # Publish the app home view
    client.views_publish(
        user_id=body["user"]["id"],
        # Home tabs must be enabled in your app configuration
        view=app_home_view,
    )


def stage_3_home_open(ack, client: WebClient, body):
    ack()

    with open("./src/app_home.json") as f:
        app_home_view = json.load(f)

    app_home_view["blocks"][0]["text"]["text"] = "Stage 3 home in progress"

    # Publish the app home view
    client.views_publish(
        user_id=body["user"]["id"],
        # Home tabs must be enabled in your app configuration
        view=app_home_view,
    )
