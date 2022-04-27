from pydantic import BaseModel
from time import time


class Workflow(BaseModel):
    id: int
    created_at: float = time()
    active: bool = True
    hostname: str = None
    start_time: int = None
