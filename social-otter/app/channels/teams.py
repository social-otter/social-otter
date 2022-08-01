from pydantic import BaseModel
from models.social import Tweet
from channels.template import BaseTemplate


class Teams(BaseTemplate):
    def __init__(self, model: BaseModel) -> None:
        super().__init__(model)

    def prep_tweet(self) -> dict:
        tweet: Tweet = self.model
        return {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "message",
                        "version": "1.5",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": tweet.content,
                                "wrap": True
                            }
                        ]
                    }
                }
            ]
        }
