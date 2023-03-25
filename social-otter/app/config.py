import os
from pydantic import BaseModel
import json
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    firbase_creds: dict = json.loads(os.getenv('FIREBASE_CREDS'))
    sentry_dsn: str = os.getenv('SENTRY_DSN')
    workflow_name: str = os.getenv('WORKFLOW_NAME')
    workflow_token: str = os.getenv('WORKFLOW_TOKEN')
    github_token: str = os.getenv('GITHUB_TOKEN')
    owner: str = 'social-otter'
    repo: str = 'social-otter'


settings = Settings()
