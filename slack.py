import logging
from decouple import config
from slack_bolt import App

logging.basicConfig(level=logging.DEBUG)

# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
app = App(token=config("SLACK_BOT_TOKEN"))

# Add functionality here

if __name__ == "__main__":
    app.start(3000)  # POST http://localhost:3000/slack/events
