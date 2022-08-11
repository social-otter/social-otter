from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, validator


class TrackingFailureLog(BaseModel):
    created_at: Optional[str]
    level: Optional[str]
    description: Optional[str]
    exception: Optional[str]

    class Config:
        validate_assignment = True

    @validator('created_at')
    def set_created_at(cls, v):
        utc = datetime.now(timezone.utc).astimezone().tzname()
        created_at = datetime.now().strftime(f"%H:%M:%S %m/%d/%Y ({utc}:00)")
        return v or created_at
