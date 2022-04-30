import sentry_sdk

from config import settings
from github.dispatch import GithubAPI

sentry_sdk.init(
    settings.sentry_dsn,
    traces_sample_rate=1.0
)


if __name__ == '__main__':
    GithubAPI().workflow_dispatch()
