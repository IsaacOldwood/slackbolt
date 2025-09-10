"""React to events in slack."""

from decouple import config
from slack_sdk.web.client import WebClient
from task_tracker import TaskTracker


def _create_support_task_from_message_reaction(
    body: dict,
    client: WebClient,
    task_tracker: TaskTracker,
) -> None:
    """Create a support task in the task tracker from a message."""

    # Get message info
    message_ts = body["event"]["item"]["ts"]
    message_channel = body["event"]["item"]["channel"]

    # Get the message content
    result = client.conversations_history(
        channel=message_channel, inclusive=True, oldest=message_ts, limit=1
    )
    message = result["messages"][0]

    # Create a permalink to the support message
    result = client.chat_getPermalink(channel=message_channel, message_ts=message_ts)
    link = result["permalink"]

    # Create the support task in the task tracker
    task_details = {
        "name": "Support Task",
        "description": message["text"] + f"\n\nLink: {link}",
        "tags": ["support"],
    }
    task_tracker.create_support_task(task_details)


def handle_reaction_added_events(body, client: WebClient):
    # Only handle clickup reactions
    emoji = body.get("event", {}).get("reaction")
    if not (emoji == "clickup"):
        return

    # Create task tracker instance
    task_tracker = TaskTracker(
        config("CLICKUP_API_KEY"), config("CLICKUP_SUPPORT_LIST_ID")
    )

    _create_support_task_from_message_reaction(body, client, task_tracker)
