from typing import List
from pydantic import BaseModel

from .tracking import Tracking
from .utm import UTM


class User(BaseModel):
    id: str
    full_name: str
    email: str
    created_at: float
    active: bool
    utm: UTM
    trackings: List[Tracking]
    workflow_name: str
