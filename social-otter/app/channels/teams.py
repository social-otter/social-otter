from channels.template import BaseTemplate


class Teams(BaseTemplate):
    def __init__(self, model) -> None:
        super().__init__(model)

    def prep_tweet(self) -> dict:
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
                                "type": "ColumnSet",
                                "columns": [
                                    {
                                        "type": "Column",
                                        "items": [
                                            {
                                                "type": "Image",
                                                "style": "Person",
                                                "url": self.model.profileImageUrl,  # noqa
                                                "altText": f"{self.model.displayname} @{self.model.username}",  # noqa
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
                                                "text": self.model.displayname,
                                                "wrap": True
                                            },
                                            {
                                                "type": "TextBlock",
                                                "spacing": "None",
                                                "text": self.model.date,
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
                                "text": self.model.content,
                                "wrap": True
                            }
                        ],
                        "actions": [
                            {
                                "type": "Action.OpenUrl",
                                "title": "Go to tweet",
                                "url": self.model.url
                            }
                        ],
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5"
                    }
                }
            ]
        }
