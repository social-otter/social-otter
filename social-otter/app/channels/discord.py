from channels.template import BaseTemplate


class Discord(BaseTemplate):
    def __init__(self, model) -> None:
        super().__init__(model)

    def prep_tweet(self) -> dict:
        avatar_url = "https://raw.githubusercontent.com/social-otter/social-otter/main/social-otter/static/images/otter.png"  # noqa
        return {
            "username": "Social Otter",
            "avatar_url": avatar_url,
            "embeds": [
                {
                    "color": 1942002,  # twitter's color
                    "author": {
                        "name": f'{self.model.displayname} @{self.model.username}',  # noqa
                        "url": self.model.url,
                        "icon_url": self.model.profileImageUrl
                    },
                    "title": 'Go to self.model',
                    "url": self.model.url,
                    "description": self.model.content,
                    "footer": {
                        "text": self.model.date
                    }
                }
            ]
        }
