from stage_1.events import _create_support_task_from_message_reaction
from slack_sdk.web.client import WebClient
from task_tracker import TaskTracker
from pytest_mock.plugin import MockerFixture


def test_create_support_task_from_message_reaction(mocker: MockerFixture):
    mock_client = mocker.MagicMock(autospec=WebClient)
    mock_client.conversations_history.return_value = {
        "messages": [{"text": "Test message text"}]
    }
    mock_client.chat_getPermalink.return_value = {
        "permalink": "https://slackapp.com/message"
    }
    mock_task_tracker = mocker.MagicMock(autospec=TaskTracker)
    test_body = {
        "event": {
            "item": {
                "ts": "12345",
                "channel": "C01234",
            }
        }
    }

    _create_support_task_from_message_reaction(
        test_body, mock_client, mock_task_tracker
    )

    mock_client.conversations_history.assert_called_once()
    mock_client.chat_getPermalink.assert_called_once()
    mock_task_tracker.create_support_task.assert_called_once()
