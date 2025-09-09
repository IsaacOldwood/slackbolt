"""Access client flow."""

from slack_sdk.web.client import WebClient
import json
from slack_bolt import App
from decouple import config
from database import Database

REQUESTS_CHANNEL_ID: str = config("SLACK_REQUESTS_CHANNEL_ID")  # type: ignore


def register_handlers(app: App):
    app.action("access_client")(open_access_client_view)
    app.action("approve_client_request")(approve_access_request)
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


def approve_access_request(ack, body, client: WebClient):
    ack()
    db = Database()

    client_name = body["actions"][0]["value"]
    user_id = body["user"]["id"]
    channel_id = body["channel"]["id"]
    message_id = body["message"]["ts"]

    db.grant_user_access(client_name, user_id)

    # Notify the user of approval
    client.chat_postMessage(
        channel=user_id,
        text=f"Your request to access {client_name} has been approved.",
    )

    # Mark request as approved
    client.chat_update(
        channel=channel_id,
        ts=message_id,
        blocks=generate_approval_message(user_id, client_name, approved=True),
    )


def generate_approval_message(user_id, client_name, approved) -> list[dict]:
    blocks = [
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"User: <@{user_id}>"},
            ],
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"Client: {client_name}",
                },
            ],
        },
    ]

    if approved:
        blocks.append(
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "Approved",
                    },
                ],
            }
        )
    else:
        blocks.append(
            {
                "type": "actions",
                "block_id": "approve_client_request",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Approve"},
                        "style": "primary",
                        "value": client_name,
                        "action_id": "approve_client_request",
                    }
                ],
            }
        )
    return blocks


def handle_submission(ack, logger, body, view, client: WebClient):
    ack()

    view_values = view["state"]["values"]
    client_name = view_values["access_client_select"]["access_client_select"][
        "selected_option"
    ]["value"]
    user_id = body["user"]["id"]

    logger.info("User: %s requests access to client %s data", user_id, client_name)

    client.chat_postMessage(
        channel=REQUESTS_CHANNEL_ID,
        text=f"USER: <@{user_id}> requests access to {client_name}",
        blocks=generate_approval_message(user_id, client_name, approved=False),
    )

    client.chat_postMessage(
        channel=user_id,
        text=f"Your request to access {client_name} has been submitted. You will receive another message when this has been approved.",
    )
