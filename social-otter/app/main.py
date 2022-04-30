import time
import sentry_sdk

from config import settings
from storage.user import get_all_users
from workers.worker import Worker
from github.dispatch import GithubAPI

sentry_sdk.init(
    settings.sentry_dsn,
    traces_sample_rate=1.0
)
MAX_RUN_TIME = 60 * 60 * 1
START_TIME = time.time()


def stop_worker():
    return (time.time() - START_TIME) > MAX_RUN_TIME


if __name__ == '__main__':
    while True:
        for user in get_all_users(workflow_name=settings.workflow_name):
            task = Worker(user=user)
            task.run()

        print(f'Waiting for 60 seconds...')
        time.sleep(60)

        if stop_worker():
            GithubAPI().workflow_dispatch()
            break
