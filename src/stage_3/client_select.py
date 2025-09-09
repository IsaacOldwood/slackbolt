"""Logic for handling the client select dropdown."""

from slack_bolt import App
from database import Database


def register_handlers(app: App):
    app.options("client_select")(show_options)
    app.action("client_select")(handle_client_select)
    app.options("refresh_tables_select")(show_options)
    app.action("refresh_tables_select")(handle_client_select)
    app.options("promote_data_select")(show_options)
    app.action("promote_data_select")(handle_client_select)
    app.options("access_client_select")(show_options)
    app.action("access_client_select")(handle_client_select)


def generate_client_options(
    db: Database, user_input: str
) -> list[dict[str, str | dict]]:
    client_list = db.fetch_client_list()

    filtered_clients = [c for c in client_list if user_input.lower() in c.lower()]

    options = [
        {
            "text": {"type": "plain_text", "text": c},
            "value": c,
        }
        for c in filtered_clients
    ]

    return options


def show_options(ack, payload):
    db = Database()

    user_input = payload.get("value")
    if user_input is None:
        return ack(options=[])

    options = generate_client_options(db, user_input)

    ack(options=options)


def handle_client_select(ack):
    ack()
    # No logic required at the moment
