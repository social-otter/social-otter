import requests

from config import settings


class GithubAPI:
    def __init__(self) -> None:
        self.base_url = f"https://api.github.com/repos/{settings.owner}/{settings.repo}"  # noqa
        self.headers = {
            'Authorization': f'Bearer {settings.workflow_token}'
        }

    def get_workflow_id(self) -> int:
        response = requests.get(
            url=f"{self.base_url}/actions/workflows",
            headers=self.headers,
        )
        if response.status_code == 200:
            data = response.json()
            for x in data['workflows']:
                if x['name'] == settings.workflow_name:
                    return x['id']
        return None

    def workflow_dispatch(self):
        worflow_id = self.get_workflow_id()

        if worflow_id:
            requests.post(
                url=f"{self.base_url}/actions/workflows/{worflow_id}/dispatches",
                headers=self.headers,
                json={"ref": "main"}
            )
