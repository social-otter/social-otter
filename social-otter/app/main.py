import time
import sentry_sdk
import socket

from config import settings
from storage.user import get_all_users
from workers.worker import Worker
from storage.workflow import WorkflowCRUD

sentry_sdk.init(
    settings.sentry_dsn,
    traces_sample_rate=1.0
)


if __name__ == '__main__':
    cycle = 60  # every minute
    hostname = socket.gethostname()

    while True:
        workflow = WorkflowCRUD(settings.workflow_id)
        w = workflow.get()
        w.hostname = hostname
        w.start_time = time.time()
        workflow.set(w)
            
        for user in get_all_users(workflow_id=settings.workflow_id):
            task = Worker(user=user)
            task.run()


        print(f'Waiting for {cycle} seconds')
        time.sleep(cycle)
