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
                        "type": "AdaptiveCard",
                        "body": [
                                {
                                    "type": "TextBlock",
                                    "size": "Medium",
                                    "weight": "Bolder",
                                    "text": f"@{tweet.username}",
                                    "wrap": True,
                                    "style": "heading"
                                },
                            {
                                    "type": "ColumnSet",
                                    "columns": [
                                        {
                                            "type": "Column",
                                            "items": [
                                                {
                                                    "type": "Image",
                                                    "style": "Person",
                                                    "url": tweet.profileImageUrl,
                                                    "altText": tweet.displayname,
                                                    "size": "Small"
                                                }
                                            ],
                                            "width": "auto"
                                        },
                                        {
                                            "type": "Column",
                                            "items": [
                                                {
                                                    "type": "TextBlock",
                                                    "weight": "Bolder",
                                                    "text": tweet.displayname,
                                                    "wrap": True
                                                },
                                                {
                                                    "type": "TextBlock",
                                                    "spacing": "None",
                                                    "text": tweet.date,
                                                    "isSubtle": True,
                                                    "wrap": True
                                                }
                                            ],
                                            "width": "stretch"
                                        }
                                    ]
                                },
                            {
                                    "type": "TextBlock",
                                    "text": "content",
                                    "wrap": True
                                }
                        ],
                        "actions": [
                            {
                                "type": "Action.OpenUrl",
                                "title": "Go to tweet",
                                "url": tweet.url
                            }
                        ],
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5"
                    }
                }
            ]
        }
