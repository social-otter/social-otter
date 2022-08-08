from typing import Optional
from pydantic import BaseModel, validator

from models.webhook import Webhook
from models.trigger import Trigger


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

    class Config:
        validate_assignment = True

    @validator('last_seen_at')
    def set_last_seen_at(cls, v):
        return v or 0
