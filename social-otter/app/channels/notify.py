from typing import Any
from pydantic import BaseModel
import requests
from models.webhook import Webhook
from channels.slack import Slack
from channels.teams import Teams


class Notify:
    def __init__(self, webhook: Webhook, model: BaseModel) -> None:
        self.webhook = webhook
        self.model = model

    def template(self) -> Any:
        if self.webhook.app == 'slack':
            return Slack(model=self.model).build_template()

        if self.webhook.app == 'teams':
            return Teams(model=self.model).build_template()

        if self.webhook.app == 'webhook':
            return self.model.dict()

    def send(self) -> None:
        return requests.post(url=self.webhook.url, json=self.template())
