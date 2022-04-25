import time
import sentry_sdk

from config import settings
from storage.user import get_all_users
from worker import Worker

sentry_sdk.init(
    settings.sentry_dsn,
    traces_sample_rate=1.0
)

if __name__ == '__main__':
    cycle = 60  # every minute

    while True:
        for user in get_all_users():
            task = Worker(user=user)
            task.run()

        print(f'Waiting for {cycle} seconds')
        time.sleep(cycle)
