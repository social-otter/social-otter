from pydantic import BaseModel
from models.social import Tweet
from channels.template import BaseTemplate


class Slack(BaseTemplate):
    def __init__(self, model: BaseModel) -> None:
        super().__init__(model)

    def prep_tweet(self) -> dict:
        tweet: Tweet = self.model
        return {
            "blocks": [
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": tweet.profileImageUrl,
                            "alt_text": tweet.displayname
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*{tweet.displayname}* <{tweet.url}|@{tweet.username}>"
                        },
                        {
                            "type": "mrkdwn",
                            "text": tweet.date
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": tweet.content
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": tweet.url
                    }
                },
                {
                    "type": "divider"
                },
            ]
        }
