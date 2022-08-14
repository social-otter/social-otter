from pydantic import BaseModel


class TrackingStats(BaseModel):
    tracking_id: str
    timestamp: int
    tweets: int
