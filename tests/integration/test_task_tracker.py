from task_tracker import TaskTracker
from decouple import config


def test_task_creation_in_list():
    api_key: str = config("CLICKUP_API_KEY")
    list_id = "901513495942"
    task_tracker = TaskTracker(api_key, list_id)
    task_details = {
        "name": "Test task",
        "description": "This is a test task to check integration",
        "assignees": [218435510],  # Isaac Oldwood
        "tags": ["support"],
    }

    result = task_tracker._create_task_in_list(list_id, task_details)

    assert result.ok
    assert result.json()["name"] == "Test task"
