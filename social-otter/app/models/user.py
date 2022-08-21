from typing import Dict, Optional
from pydantic import BaseModel

from models.tracking import Tracking


class User(BaseModel):
    id: str
    full_name: str
    created_at: float
    trackings: Dict[str, Tracking]
    workflow_name: Optional[str]
