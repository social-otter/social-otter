from typing import Dict, Optional
from pydantic import BaseModel
from models.tracking_history import TrackingHistory
from models.twitter_user import TwitterUser


class TrackingUpdateHistory(BaseModel):
    found_user: Optional[TwitterUser]
    history: Optional[TrackingHistory]


class TrackingUpdate(BaseModel):
    trackings: Dict[str, TrackingUpdateHistory]
