# slackbolt
Code for SlackBolt talk at PyCon UK 2025

## First time setup

1. Install `uv`
2. Create a `.env`
3. Create venv with `uv sync`

## Running the slack app

```shell
uv run ./src/slack.py
```

## Environment variables

```text
CLICKUP_API_KEY="#############"
CLICKUP_SUPPORT_LIST_ID="####################"

SLACK_BOT_TOKEN="#####################"
SLACK_SIGNING_SECRET="################"
```

## Testing

This skips all integration tests by default
```shell
uv run pytest
```

To Include them run

```shell
uv run pytest tests tests/integration
```