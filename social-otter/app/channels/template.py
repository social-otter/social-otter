from pydantic import BaseModel
from models.social import Tweet


class BaseTemplate:
    def __init__(self, model: BaseModel) -> None:
        self.model = model

    def prep_tweet(self) -> dict:
        ...

    def build_template(self):
        if isinstance(self.model, Tweet):
            return self.prep_tweet()
