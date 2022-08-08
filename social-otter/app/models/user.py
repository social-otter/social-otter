from typing import List, Optional
from pydantic import BaseModel

from models.tracking import Tracking


class User(BaseModel):
    id: str
    full_name: str
    created_at: float
    trackings: List[Tracking]
    workflow_name: Optional[str]
