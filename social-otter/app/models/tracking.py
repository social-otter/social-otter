from typing import Optional
from pydantic import BaseModel, validator

from models.webhook import Webhook
from models.trigger import Trigger
from models.twitter_user import TwitterUser


class Tracking(BaseModel):
    id: str
    application: str
    active: bool
    account: str
    last_seen_at: Optional[int]
    last_seen_at_friendly: Optional[str]
    webhooks: Optional[Webhook]
    trigger: Trigger
    elapsed_ms: Optional[float]
    count: Optional[int]
    last_execution_at: Optional[str]
    found_user: Optional[TwitterUser]

    class Config:
        validate_assignment = True

    @validator('last_seen_at')
    def set_last_seen_at(cls, v):
        return v or 0
