import threading
from time import time
from datetime import datetime, timezone
from typing import List
from storage.user import UserCRUD
from integrations.twitter import Twitter
from models.user import User
from models.tracking import Tracking
from models.webhook import Webhook
from models.tracking_failure_log import TrackingFailureLog
from channels.notify import Notify
from utils.termcolors import color
from utils.dateops import friendly_datetime


class Worker(threading.Thread):
    def __init__(self, user: User) -> None:
        threading.Thread.__init__(self)
        self.user = user
        self.modified = False
        print(f'Worker started for {color.WARNING}<{self.user.id}>{color.END}')

    def send_notify(self, webhook: Webhook, model):
        return Notify(webhook=webhook, model=model).send()

    def twitter(self, track: Tracking) -> Tracking:
        start_time = time()
        tw = Twitter(tracking=track)
        tweet_counts, tweets = tw.grab_new_tweets()
        utc = datetime.now(timezone.utc).astimezone().tzname()
        track.last_execution_at = datetime.now().strftime(f"%H:%M:%S ({utc}:00)")
        track.count = tweet_counts
        track.found_user = tw.get_user()

        if len(tweets) > 0:
            self.modified = True
            track.elapsed_ms = round(time()-start_time, 3)
            track.last_seen_at = max([i.tweet_at for i in tweets], default=0)
            track.last_seen_at_friendly = friendly_datetime(track.last_seen_at)
            for tweet in sorted(tweets, key=lambda x: x.tweet_at):
                try:
                    response = self.send_notify(webhook=track.webhooks, model=tweet)

                    if response.status_code not in [200, 201]:
                        raise ValueError('Notification was not sent!')
                except Exception as e:
                    track.failure_log.append(
                        TrackingFailureLog(
                            level='critical',
                            description='Notification method invalid',
                            exception=str(e)
                        )
                    )
                    # No more add to log
                    # Stopping the process
                    break
            return track
        return track

    def build_tracker(self, track: Tracking) -> Tracking:
        if track.active:
            if track.application == 'twitter':
                return self.twitter(track=track)

            if track.application == 'facebook':
                ...

            if track.application == 'instagram':
                ...
        else:
            print(f'{color.FAIL}Tracking is not active!{color.END}')
            return track

    def process(self):
        trackings: List[Tracking] = []
        for track in self.user.trackings:
            track.failure_log = []  # initial value
            _track = self.build_tracker(track=track)
            trackings.append(_track)

        self.user.trackings = trackings

        # Prevent redundant update (minimize firebase cost)
        # Update if the model has changed or has an error
        if self.modified or any([x.failure_log for x in trackings]):
            UserCRUD(doc_id=self.user.id).set_user_doc(self.user)
            print(f'{color.OKGREEN}Document changed <{self.user.id}>{color.END}')
        else:
            print(f'{color.FAIL}There are no changes.{color.END}')

    def run(self):
        self.process()
