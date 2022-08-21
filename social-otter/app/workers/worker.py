from pprint import pprint
import threading
from time import time
from storage.user import UserCRUD
from integrations.twitter import Twitter
from models.user import User
from models.tracking import Tracking
from models.webhook import Webhook
from models.tracking_update import TrackingUpdate, TrackingUpdateHistory
from models.tracking_history import TrackingHistory
from models.tracking_twitter_misc import TrackingTwitterMisc
from models.tracking_failure_log import TrackingFailureLog
from channels.notify import Notify
from utils.termcolors import color


class Worker(threading.Thread):
    def __init__(self, user: User) -> None:
        threading.Thread.__init__(self)
        self.user = user
        self.errors = []
        print(f'Worker started for {color.WARNING}<{self.user.id}>{color.END}')

    def send_notify(self, webhook: Webhook, model):
        return Notify(webhook=webhook, model=model).send()

    def twitter(self, track: Tracking) -> TrackingUpdateHistory:
        tw = Twitter(tracking=track)
        stats, tweets = tw.grab_new_tweets()
        last_tweet_id = sorted(tweets, key=lambda x: x.id)[-1].id if len(tweets) > 0 else 0
        all_stats = []

        if track.history:
            if track.history.stats:
                all_stats = track.history.stats
        
        all_stats.append(stats)

        # Notify to channels
        for tweet in sorted(tweets, key=lambda x: x.id):
            try:
                response = self.send_notify(webhook=track.webhooks, model=tweet)
                
                if not 200 <= response.status_code <= 299:
                    print(color.FAIL, response.status_code, color.END)
                    print(color.FAIL, response.text, color.END)
                    raise ValueError('Notification was not sent!')
            except Exception as e:
                self.errors.append(
                    TrackingFailureLog(
                        level='critical',
                        description='Notification method invalid',
                        exception=str(e)
                    )
                )
                # No more add to log
                # Stopping the process
                break
        
        history = TrackingHistory(
            misc=TrackingTwitterMisc(
                last_track_at=time(),
                last_tweet_id=last_tweet_id,
            ),
            stats=all_stats,
            errors=self.errors
        )
        found_user = tw.get_user()

        return TrackingUpdateHistory(found_user=found_user, history=history)

    def build_tracker(self, track: Tracking) -> TrackingUpdateHistory:
        if track.application == 'twitter':
            return self.twitter(track=track)

        if track.application == 'facebook':
            ...

        if track.application == 'instagram':
            ...

    def process(self):
        update = {}
        for k, v in self.user.trackings.items():
            tracking_id = k
            track: Tracking = v

            if track.active:
                update[tracking_id] = self.build_tracker(track=track)
        
        if len(list(update.keys())) > 0:
            UserCRUD(doc_id=self.user.id).merge_tracking(
                tracking=TrackingUpdate(trackings=update)
            )
            print(f'{color.OKGREEN}Document changed <{self.user.id}>{color.END}')

    def run(self):
        self.process()
