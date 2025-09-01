"""Change client flow."""

from slack_sdk.web.client import WebClient
import json
from slack_bolt import App


def register_handlers(app: App):
    app.action("change_client")(open_change_client_view)
    app.view("stage_3_change_client")(handle_submission)


def open_change_client_view(ack, body, client: WebClient):
    ack()
    with open("./src/stage_3/views/change_client.json") as f:
        change_client_view = json.load(f)

    # Publish the app home view
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view=change_client_view,
    )


def handle_submission(ack, logger, body, view, client: WebClient):
    ack()
    # ToDo: Logic to hit an external API to change the select client in the internal dashboard
    view_values = view["state"]["values"]
    client_name = view_values["client_select"]["client_select"]["selected_option"][
        "value"
    ]
    user_id = body["user"]["id"]
    logger.info("User: %s changed client to: %s", user_id, client_name)

    client.chat_postMessage(
        channel=user_id, text=f"Changed dashboard client to: {client_name}"
    )
