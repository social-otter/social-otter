from pydantic import BaseModel


class Tweet(BaseModel):
    id: int
    content: str
    date: str
    url: str
    username: str
    displayname: str
    profileImageUrl: str
    tweet_at: int
