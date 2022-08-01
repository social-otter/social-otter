from typing import List
from pydantic import BaseModel

from models.tracking import Tracking


class User(BaseModel):
    id: str
    full_name: str
    email: str
    created_at: float
    active: bool
    trackings: List[Tracking]
    workflow_name: str
