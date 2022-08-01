from typing import Optional
from pydantic import BaseModel

from models.webhook import Webhook
from models.trigger import Trigger


class Tracking(BaseModel):
    application: str
    active: bool
    account: str
    last_seen_at: int
    last_seen_at_friendly: str
    webhooks: Optional[Webhook]
    trigger: Trigger
    elapsed_ms: float = 0
