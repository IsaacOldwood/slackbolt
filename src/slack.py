import logging
from decouple import config
from slack_bolt import App
from events import handle_reaction_added_events
from app_home import update_home_tab
from actions import open_stage_2_create_task_view
from views import handle_submission

logging.basicConfig(level=logging.DEBUG)

app = App(
    token=config("SLACK_BOT_TOKEN"), signing_secret=config("SLACK_SIGNING_SECRET")
)

app.event("reaction_added")(handle_reaction_added_events)
app.event("app_home_opened")(update_home_tab)
app.action("open_create_task_view")(open_stage_2_create_task_view)
app.view("stage_2_create_task")(handle_submission)

if __name__ == "__main__":
    app.start(3000)  # POST http://localhost:3000/slack/events
