import threading
from time import time
from datetime import datetime, timezone
from storage.user import UserCRUD
from integrations.twitter import Twitter
from models.user import User
from models.tracking import Tracking
from models.webhook import Webhook
from channels.notify import Notify
from utils.termcolors import color
from utils.dateops import friendly_datetime


class Worker(threading.Thread):
    def __init__(self, user: User) -> None:
        threading.Thread.__init__(self)
        self.user = user
        self.modified = False
        print(f'Worker started for {color.WARNING}<{self.user.id}>{color.END}')

    def send_notify(self, webhook: Webhook, model) -> None:
        return Notify(webhook=webhook, model=model).send()

    def twitter(self, track: Tracking) -> Tracking:
        start_time = time()
        tweet_counts, tweets = Twitter(tracking=track).grab_new_tweets()
        utc = datetime.now(timezone.utc).astimezone().tzname()
        track.last_execution_at = datetime.now().strftime(f"%H:%M:%S ({utc}:00)")
        track.count = tweet_counts

        if len(tweets) > 0:
            self.modified = True
            track.elapsed_ms = round(time()-start_time, 3)
            track.last_seen_at = max([i.tweet_at for i in tweets], default=0)
            track.last_seen_at_friendly = friendly_datetime(track.last_seen_at)
            for tweet in sorted(tweets, key=lambda x: x.tweet_at):
                self.send_notify(webhook=track.webhooks, model=tweet)
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

    def process(self):
        trackings = []
        for track in self.user.trackings:
            _track = self.build_tracker(track=track)
            trackings.append(_track)

        self.user.trackings = trackings

        if self.modified:
            UserCRUD(doc_id=self.user.id).set_user_doc(self.user)
            print(f'{color.OKGREEN}Document changed <{self.user.id}>{color.END}')
        else:
            print(f'{color.FAIL}There are no changes.{color.END}')

    def run(self):
        self.process()
