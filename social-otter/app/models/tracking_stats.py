from pydantic import BaseModel


class TrackingStats(BaseModel):
    timestamp: int
    elapsed_sec: int
    count: int
    detail: dict
