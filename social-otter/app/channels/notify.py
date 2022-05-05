from typing import Any
import requests
from models.webhook import Webhook
from .slack import Slack
from .teams import Teams


class Notify:
    def __init__(self, webhook: Webhook, model: Any) -> None:
        self.webhook = webhook
        self.model = model

    def template(self) -> Any:
        if self.webhook.app == 'slack':
            return Slack(model=self.model).build_template()

        if self.webhook.app == 'teams':
            return Teams(model=self.model).build_template()

    def send(self) -> None:
        requests.post(url=self.webhook.url, json=self.template())
