import logging
from decouple import config
from slack_bolt import App

logging.basicConfig(level=logging.DEBUG)

app = App(
    token=config("SLACK_BOT_TOKEN"), signing_secret=config("SLACK_SIGNING_SECRET")
)

@app.event("reaction_added")
def handle_reaction_added_events(body, logger):
    emoji = body.get('event', {}).get('reaction')
    if not (emoji == 'clickup'):
        return
    else:
        logger.debug(body)

if __name__ == "__main__":
    app.start(3000)  # POST http://localhost:3000/slack/events
