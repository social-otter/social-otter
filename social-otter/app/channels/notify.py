from typing import Any
from pydantic import BaseModel
import requests
from requests import Response
from channels.slack import Slack
from channels.teams import Teams
from channels.discord import Discord
from models.webhook import Webhook


class Notify:
    def __init__(self, webhook: Webhook, model: BaseModel) -> None:
        self.webhook = webhook
        self.model = model

    def template(self) -> Any:
        templates = {
            "slack": Slack(model=self.model).build_template(),
            "teams": Teams(model=self.model).build_template(),
            "discord": Discord(model=self.model).build_template(),
            "webhook": self.model.dict()
        }

        return templates.get(self.webhook.app)

    def send(self) -> Response:
        return requests.post(url=self.webhook.url, json=self.template())
