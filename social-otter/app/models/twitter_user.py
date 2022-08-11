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
