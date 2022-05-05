import threading
import time
import sentry_sdk

from config import settings
from storage.user import get_all_users, UserCRUD
from workers.worker import Worker
from github.dispatch import GithubAPI

sentry_sdk.init(
    settings.sentry_dsn,
    traces_sample_rate=1.0
)
WAIT_SECONDS = 60 * 5 # every 5 minute
MAX_RUN_TIME = 60 * 60 * 5
START_TIME = time.time()


def stop_worker():
    return (time.time() - START_TIME) > MAX_RUN_TIME


if __name__ == '__main__':
    while True:
        threads = []
        for user in get_all_users(workflow_name=settings.workflow_name):
            task: threading.Thread = Worker(user=user)
            threads.append(task)
            task.start()
        
        for thread in threads:
            thread.join()

        print(f'Waiting for {WAIT_SECONDS} seconds...')
        time.sleep(WAIT_SECONDS)

        if stop_worker():
            GithubAPI().workflow_dispatch()
            break
