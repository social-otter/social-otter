import time
import sentry_sdk
import socket

from config import settings
from storage.user import get_all_users
from worker import Worker
from storage.workflow import WorkflowCRUD

sentry_sdk.init(
    settings.sentry_dsn,
    traces_sample_rate=1.0
)

def update_workflow():
    workflow = WorkflowCRUD(settings.workflow_id)
    w = workflow.get()
    w.hostname = socket.gethostname()
    w.start_time = time.time()
    workflow.set(w)


if __name__ == '__main__':
    cycle = 60  # every minute
    update_workflow()

    while True:
        for user in get_all_users(workflow_id=settings.workflow_id):
            task = Worker(user=user)
            task.run()

        print(f'Waiting for {cycle} seconds')
        time.sleep(cycle)
