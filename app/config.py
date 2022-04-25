import os
import json
from pydantic import BaseModel


class Settings(BaseModel):
    firbase_creds: dict = json.loads(os.getenv('FIREBASE_CREDS'))
    sentry_dsn: str = os.getenv('SENTRY_DSN')


settings = Settings()
