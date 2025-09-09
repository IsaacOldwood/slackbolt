"""Logic for handling the client select dropdown."""

from slack_bolt import App
from database import Database


def register_handlers(app: App):
    app.options("promote_data_project_select")(show_options)
    app.action("promote_data_project_select")(handle_client_select)


def generate_project_options(
    db: Database, user_input: str
) -> list[dict[str, str | dict]]:
    project_list = db.fetch_project_list()

    filtered_projects = [p for p in project_list if user_input.lower() in p.lower()]

    options = [
        {
            "text": {"type": "plain_text", "text": p},
            "value": p,
        }
        for p in filtered_projects
    ]

    return options


def show_options(ack, payload, body):
    db = Database()

    user_input = payload.get("value")
    if user_input is None:
        return ack(options=[])

    options = generate_project_options(db, user_input)

    ack(options=options)


def handle_client_select(ack):
    ack()
    # No logic required at the moment
