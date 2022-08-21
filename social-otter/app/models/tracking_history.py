from typing import List, Optional
from pydantic import BaseModel
from models.tracking_failure_log import TrackingFailureLog
from models.tracking_stats import TrackingStats
from models.tracking_twitter_misc import TrackingTwitterMisc


class TrackingHistory(BaseModel):
    misc: TrackingTwitterMisc
    stats: Optional[List[TrackingStats]]
    errors: Optional[List[TrackingFailureLog]]
