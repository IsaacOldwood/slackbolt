import logging
from decouple import config
from slack_bolt import App
from events import handle_reaction_added_events

logging.basicConfig(level=logging.DEBUG)

app = App(
    token=config("SLACK_BOT_TOKEN"), signing_secret=config("SLACK_SIGNING_SECRET")
)

app.event("reaction_added")(handle_reaction_added_events)

if __name__ == "__main__":
    app.start(3000)  # POST http://localhost:3000/slack/events
