from typing import Optional
from pydantic import BaseModel

from models.webhook import Webhook
from models.trigger import Trigger
from models.twitter_user import TwitterUser
from models.tracking_history import TrackingHistory


class Tracking(BaseModel):
    id: str
    application: str
    active: bool
    keyword: str
    webhooks: Webhook
    trigger: Trigger
    found_user: Optional[TwitterUser]
    history: Optional[TrackingHistory]
