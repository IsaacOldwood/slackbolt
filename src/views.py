"""Handle view submission."""

# Update the view on submission


def handle_submission(ack, say):
    # The build_new_view() method returns a modal view
    # To build a modal view, we recommend using Block Kit Builder:
    # https://app.slack.com/block-kit-builder/#%7B%22type%22:%22modal%22,%22callback_id%22:%22view_1%22,%22title%22:%7B%22type%22:%22plain_text%22,%22text%22:%22My%20App%22,%22emoji%22:true%7D,%22blocks%22:%5B%5D%7D
    ack()
