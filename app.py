from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_app import app
from fastapi import FastAPI, Request

app_handler = SlackRequestHandler(app)

api = FastAPI()


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)
