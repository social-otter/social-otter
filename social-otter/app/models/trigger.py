from typing import Optional
from pydantic import BaseModel


class Trigger(BaseModel):
    post_to_this_by_mention: Optional[bool]
    post_to_this_by_hashtag: Optional[bool]
    post_from_this: Optional[bool]
