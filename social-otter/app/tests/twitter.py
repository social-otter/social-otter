import snscrape.modules.twitter as tw
from pprint import pprint
from typing import Optional
from pydantic import BaseModel


class TwitterUser(BaseModel):
    id: int
    username: str
    description: Optional[str]
    verified: Optional[bool]
    displayname: Optional[str]
    favouritesCount: Optional[int]
    followersCount: Optional[int]
    friendsCount: Optional[int]
    mediaCount: Optional[int]
    profileBannerUrl: Optional[str]
    profileImageUrl: Optional[str]


def find_user():
    results = tw.TwitterUserScraper('POTUS')._get_entity()
    if isinstance(results, tw.User):
        data = TwitterUser(**results.__dict__)
        pprint(data.dict(), indent=4)


find_user()
