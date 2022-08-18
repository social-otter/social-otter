import threading
from time import time
from typing import List
from storage.user import UserCRUD
from integrations.twitter import Twitter
from models.user import User
from models.tracking import Tracking
from models.webhook import Webhook
from models.tracking_failure_log import TrackingFailureLog
from models.tracking_history import TrackingHistory
from models.tracking_twitter_misc import TrackingTwitterMisc
from channels.notify import Notify
from utils.termcolors import color


class Worker(threading.Thread):
    def __init__(self, user: User) -> None:
        threading.Thread.__init__(self)
        self.user = user
        print(f'Worker started for {color.WARNING}<{self.user.id}>{color.END}')

    def send_notify(self, webhook: Webhook, model):
        return Notify(webhook=webhook, model=model).send()

    def twitter(self, track: Tracking) -> Tracking:
        t0 = time()
        tw = Twitter(tracking=track)
        elapsed_sec = int(time()-t0)
        tweets = tw.grab_new_tweets()
        last_tweet_id = None

        if len(tweets) > 0:
            last_tweet_id = sorted(tweets, key=lambda x: x.id)[-1].id

        track.misc = TrackingTwitterMisc(
            last_tweet_id=last_tweet_id or 0,
            last_track_at=time()
        )
        history = TrackingHistory(
            timestamp=time(),
            elapsed_sec=elapsed_sec,
            count=len(tweets)
        )
        track.history = track.history.append(history) if track.history else [history]
        track.found_user = tw.get_user()

        # Notify to channels
        for tweet in sorted(tweets, key=lambda x: x.id):
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

    def build_tracker(self, track: Tracking) -> Tracking:
        if track.active:
            if track.application == 'twitter':
                return self.twitter(track=track)

            if track.application == 'facebook':
                ...

            if track.application == 'instagram':
                ...
        
        return track

    def process(self):
        trackings: List[Tracking] = []
        for track in self.user.trackings:
            track.failure_log = []  #  initial value
            _track = self.build_tracker(track=track)
            trackings.append(_track)

        self.user.trackings = trackings
        UserCRUD(doc_id=self.user.id).set_user_doc(self.user)
        print(f'{color.OKGREEN}Document changed <{self.user.id}>{color.END}')

    def run(self):
        self.process()
