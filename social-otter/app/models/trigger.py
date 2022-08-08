from typing import Optional
from pydantic import BaseModel


class Trigger(BaseModel):
    post_to_this_by_mention: bool
    post_to_this_by_hashtag: bool
    post_from_this: bool
