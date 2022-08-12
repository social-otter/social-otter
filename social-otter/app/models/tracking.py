from typing import List, Optional
from pydantic import BaseModel, validator

from models.webhook import Webhook
from models.trigger import Trigger
from models.twitter_user import TwitterUser
from models.tracking_failure_log import TrackingFailureLog


class Tracking(BaseModel):
    id: str
    application: str
    active: Optional[bool] = True
    account: str
    last_seen_at: Optional[int] = 0
    last_seen_at_friendly: Optional[str]
    webhooks: Optional[Webhook]
    trigger: Trigger
    elapsed_ms: Optional[float]
    count: Optional[int]
    last_execution_at: Optional[str]
    found_user: Optional[TwitterUser]
    failure_log: Optional[List[TrackingFailureLog]]

    class Config:
        validate_assignment = True

    @validator('last_seen_at')
    def set_last_seen_at(cls, v):
        return v or 0

    @validator('active')
    def set_active(cls, v):
        return v or True
