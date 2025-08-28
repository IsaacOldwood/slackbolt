"""React to button actions."""

from slack_sdk.web.client import WebClient
import json


def open_create_task_view(ack, body, client: WebClient):
    ack()
    with open("./src/stage_2/views/create_task.json") as f:
        create_task_view = json.load(f)

    # Publish the app home view
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view=create_task_view,
    )
