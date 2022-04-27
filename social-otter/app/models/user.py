from typing import List, Optional
from pydantic import BaseModel


class Webhook(BaseModel):
    app: str
    url: str


class Trigger(BaseModel):
    post_to_this_by_mention: Optional[bool]
    post_to_this_by_hashtag: Optional[bool]
    post_from_this: Optional[bool]


class Tracking(BaseModel):
    application: str
    account: str
    last_seen_at: int
    webhooks: Optional[Webhook]
    trigger: Trigger


class UTM(BaseModel):
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_campaign: Optional[str]
    utm_term: Optional[str]
    utm_content: Optional[str]


class User(BaseModel):
    id: str
    full_name: str
    email: str
    created_at: float
    active: bool
    utm: UTM
    trackings: List[Tracking]
    workflow_id: int
