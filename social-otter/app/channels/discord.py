from pydantic import BaseModel
from models.social import Tweet
from channels.template import BaseTemplate


class Discord(BaseTemplate):
    def __init__(self, model: BaseModel) -> None:
        super().__init__(model)

    def prep_tweet(self) -> dict:
        tweet: Tweet = self.model
        avatar_url = "https://raw.githubusercontent.com/social-otter/social-otter/main/social-otter/static/images/otter.png"
        return {
            "username": "Social Otter",
            "avatar_url": avatar_url,
            "embeds": [
                {
                    "color": 1942002,  # twitter's color
                    "author": {
                        "name": f'{tweet.displayname} @{tweet.username}',
                        "url": tweet.url,
                        "icon_url": tweet.profileImageUrl
                    },
                    "title": 'Go to tweet',
                    "url": tweet.url,
                    "description": tweet.content,
                    "footer": {
                        "text": tweet.date
                    }
                }
            ]
        }
