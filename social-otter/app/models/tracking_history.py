from pydantic import BaseModel


class TrackingHistory(BaseModel):
    timestamp: int
    elapsed_sec: int
    count: int
