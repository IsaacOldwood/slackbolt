import logging
from decouple import config
from slack_bolt import App
from stage_2.events import handle_reaction_added_events
from app_home import initial_home_open, stage_2_home_open, stage_3_home_open
from stage_2.actions import open_create_task_view
from stage_2.views import handle_submission

logging.basicConfig(level=logging.DEBUG)

app = App(
    token=config("SLACK_BOT_TOKEN"), signing_secret=config("SLACK_SIGNING_SECRET")
)

app.event("reaction_added")(handle_reaction_added_events)
app.event("app_home_opened")(initial_home_open)
app.action("open_stage_2_home")(stage_2_home_open)
app.action("open_stage_3_home")(stage_3_home_open)
app.action("open_create_task_view")(open_create_task_view)
app.view("stage_2_create_task")(handle_submission)

if __name__ == "__main__":
    app.start(3000)  # POST http://localhost:3000/slack/events
