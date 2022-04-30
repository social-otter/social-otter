from pydantic import BaseModel


class Webhook(BaseModel):
    app: str
    url: str
