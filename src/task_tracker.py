import requests


class TaskTracker:
    """Integrate with a task tracking tool, currently ClickUp."""

    def __init__(self, api_key: str, support_list_id: str):
        """Create instance with api key and other key details."""
        self.api_key = api_key
        self.support_list_id = support_list_id

    def _create_task_in_list(self, list_id: str, task_details: dict[str, str]):
        """Create a new task in a given list."""
        url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
        headers = {"Authorization": self.api_key}
        # payload = {"name": "Test Ticket"}
        return requests.post(url=url, headers=headers, json=task_details)

    def create_support_task(self, task_details: dict[str, str]):
        """Create a task in the pre-defined support list."""
        return self._create_task_in_list(self.support_list_id, task_details)
