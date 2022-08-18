from ctypes import Union
from typing import List, Optional
from pydantic import BaseModel, validator

from models.webhook import Webhook
from models.trigger import Trigger
from models.twitter_user import TwitterUser
from models.tracking_failure_log import TrackingFailureLog
from models.tracking_history import TrackingHistory
from models.tracking_twitter_misc import TrackingTwitterMisc


class Tracking(BaseModel):
    id: str
    application: str
    active: Optional[bool] = True
    keyword: str
    webhooks: Optional[Webhook]
    trigger: Trigger
    found_user: Optional[TwitterUser]
    failure_log: Optional[List[TrackingFailureLog]]
    history: Optional[List[TrackingHistory]]
    misc: Optional[TrackingTwitterMisc]

    class Config:
        validate_assignment = True

    @validator('active')
    def set_active(cls, v):
        return v or True
