import requests
from decouple import config

CLICKUP_SUPPORT_LIST_ID = config("CLICKUP_SUPPORT_LIST_ID")
url = f"https://api.clickup.com/api/v2/list/{CLICKUP_SUPPORT_LIST_ID}/task"
headers = {"Authorization": config("CLICKUP_API_KEY")}
payload = {"name": "Test Ticket"}

r = requests.post(url=url, headers=headers, json=payload)

print(r.text)
