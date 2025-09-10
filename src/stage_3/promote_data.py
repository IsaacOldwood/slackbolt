"""Promote data flow."""

from slack_sdk.web.client import WebClient
import json
from slack_bolt import App
from decouple import config

REQUESTS_CHANNEL_ID: str = config("SLACK_REQUESTS_CHANNEL_ID")  # type: ignore


def register_handlers(app: App):
    app.action("promote_data")(open_promote_data_view)
    app.view("stage_3_promote_data")(handle_submission)


def open_promote_data_view(ack, body, client: WebClient):
    ack()
    with open("./src/stage_3/views/promote_data.json") as f:
        promote_data_view = json.load(f)

    # Publish the app home view
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view=promote_data_view,
    )


def generate_promote_sql(client, project):
    """Generate the SQL for devs to run promote data flow"""
    client = client.lower().replace(' ','_').replace('-','_')
    project = project.lower().replace(' ','_').replace('-','_')
    sql = (
        f"INSERT INTO {client}.{project}.prod SELECT * FROM {client}.{project}.valid_data "
        f"\nWHERE (SELECT project_id FROM {client}.meta.projects WHERE project_name = '{project}') NOT IN "
        f"\n(SELECT project_id FROM {client}.{project}.prod);"
    )

    return sql


def handle_submission(ack, logger, body, view, client: WebClient):
    ack()

    view_values = view["state"]["values"]
    client_name = view_values["promote_data_select"]["promote_data_select"][
        "selected_option"
    ]["value"]
    project_name = view_values["promote_data_project_select"][
        "promote_data_project_select"
    ]["selected_option"]["value"]
    user_id = body["user"]["id"]

    logger.info(
        "User: %s requested %s %s data to be promoted",
        user_id,
        client_name,
        project_name,
    )

    # Generate SQL and post to channel
    sql = generate_promote_sql(client_name, project_name)

    client.chat_postMessage(
        channel=REQUESTS_CHANNEL_ID, text=f"USER: <@{user_id}>\n```{sql}```"
    )

    client.chat_postMessage(
        channel=user_id,
        text=f"Request submitted for data promotion for {client_name} {project_name}",
    )
