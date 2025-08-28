"""Handle view submission."""

from slack_sdk.web.client import WebClient
from task_tracker import TaskTracker
from decouple import config


def _create_task_from_view_submission(
    body, view, task_tracker: TaskTracker, client: WebClient
):
    view_values = view["state"]["values"]
    task_title = view_values["task_title"]["task_title_text"]["value"]
    task_desc = view_values["task_desc"]["task_desc_text"]["value"]
    user = body["user"]["id"]

    # Create the support task in the task tracker
    task_details = {
        "name": task_title,
        "description": task_desc,
        "tags": ["support"],
    }
    task = task_tracker.create_support_task(task_details)

    if not task.ok:
        msg = "Error creating support task"
    else:
        task_url = task.json()["url"].replace("https", "clickup")
        msg = f"Support task created: {task_url}"

    # Message the user with a link to their ticket
    client.chat_postMessage(channel=user, text=msg)


def handle_submission(ack, body, client: WebClient, view):
    # Validate the inputs
    task_title = view["state"]["values"]["task_title"]["task_title_text"]["value"]
    errors = {}
    if task_title is not None and len(task_title) <= 5:
        errors["task_title"] = "The value must be longer than 5 characters"
        ack(response_action="errors", errors=errors)
        return

    ack()

    # Create task tracker instance
    task_tracker = TaskTracker(
        config("CLICKUP_API_KEY"), config("CLICKUP_SUPPORT_LIST_ID")
    )

    _create_task_from_view_submission(body, view, task_tracker, client)
