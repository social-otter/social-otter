import os
import json
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    firbase_creds: dict = json.loads(os.getenv('FIREBASE_CREDS'))
    sentry_dsn: str = os.getenv('SENTRY_DSN')
    workflow_id: str = os.getenv('WORKFLOW_ID')


settings = Settings()
