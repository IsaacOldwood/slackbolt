"""Access client flow."""

from slack_sdk.web.client import WebClient
import json
from slack_bolt import App


def register_handlers(app: App):
    app.action("access_client")(open_access_client_view)
    app.view("stage_3_access_client")(handle_submission)


def open_access_client_view(ack, body, client: WebClient):
    ack()
    with open("./src/stage_3/views/access_client.json") as f:
        access_client_view = json.load(f)

    # Publish the app home view
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view=access_client_view,
    )


def handle_submission(ack, logger, body, view, client: WebClient):
    ack()

    view_values = view["state"]["values"]
    client_name = view_values["access_client_select"]["access_client_select"][
        "selected_option"
    ]["value"]
    user_id = body["user"]["id"]

    logger.info("User: %s requests access to client %s data", user_id, client_name)

    client.chat_postMessage(
        channel=user_id,
        text=f"Your request to access {client_name} has been submitted. You will receive another message when this has been approved.",
    )
