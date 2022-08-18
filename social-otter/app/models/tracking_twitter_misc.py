from pydantic import BaseModel


class TrackingTwitterMisc(BaseModel):
    last_tweet_id: int
    last_track_at: int
