from channels.template import BaseTemplate


class Slack(BaseTemplate):
    def __init__(self, model) -> None:
        super().__init__(model)

    def prep_tweet(self) -> dict:
        return {
            "blocks": [
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": self.model.profileImageUrl,
                            "alt_text": self.model.displayname
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*{self.model.displayname}* <{self.model.url}|@{self.model.username}>"  # noqa
                        },
                        {
                            "type": "mrkdwn",
                            "text": self.model.date
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": self.model.content
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": self.model.url
                    }
                },
                {
                    "type": "divider"
                },
            ]
        }
