"""Refresh client data flow."""

from slack_sdk.web.client import WebClient
import json
from slack_bolt import App
from database import Database


def register_handlers(app: App):
    app.action("refresh_tables")(open_refresh_tables_view)
    app.view("stage_3_refresh_tables")(handle_submission)


def open_refresh_tables_view(ack, body, client: WebClient):
    ack()
    with open("./src/stage_3/views/refresh_tables.json") as f:
        refresh_tables_view = json.load(f)

    # Publish the app home view
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view=refresh_tables_view,
    )


def handle_submission(ack, logger, body, view, client: WebClient):
    ack()
    db = Database()

    view_values = view["state"]["values"]
    client_name = view_values["refresh_tables_select"]["refresh_tables_select"][
        "selected_option"
    ]["value"]
    user_id = body["user"]["id"]

    logger.info("User: %s refreshed client %s data", user_id, client_name)

    db.refresh_client_data(client_name)

    client.chat_postMessage(
        channel=user_id,
        text=f"Refreshed {client_name} data. The internal dashboard will now be up to date",
    )
