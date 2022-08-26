import threading
from time import time, mktime
from datetime import datetime
from typing import List, Tuple
from storage.user import UserCRUD
from integrations.twitter import Twitter
from models.user import User
from models.tracking import Tracking
from models.webhook import Webhook
from models.tracking_update import TrackingUpdate, TrackingUpdateHistory
from models.tracking_history import TrackingHistory
from models.tracking_twitter_misc import TrackingTwitterMisc
from models.tracking_failure_log import TrackingFailureLog
from models.tracking_stats import TrackingStats
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

    def twitter(self, track: Tracking) -> Tuple[TrackingStats, TrackingUpdateHistory]:
        tw = Twitter(tracking=track)
        stats, tweets = tw.grab_new_tweets()
        last_tweet_id = sorted(tweets, key=lambda x: x.id)[-1].id if len(tweets) > 0 else 0
        all_stats: List[TrackingStats] = []

        if track.history:
            if track.history.stats:
                all_stats = track.history.stats

        all_stats.append(stats)

        # Filtered Daily Tweets
        if len(all_stats) > 0:
            today = datetime.now().date()
            today_timestamp = int(mktime(today.timetuple()))
            filtered_stats = [x for x in all_stats if x.timestamp >= today_timestamp]
            all_stats = list(sorted(filtered_stats, key=lambda x: x.timestamp))

        # Notify to channels
        for tweet in sorted(tweets, key=lambda x: x.id):
            try:
                response = self.send_notify(webhook=track.webhooks, model=tweet)

                if not 200 <= response.status_code <= 299:
                    raise ValueError('Notification was not sent!')
            except Exception as e:
                self.errors.append(
                    TrackingFailureLog(
                        level='critical',
                        description='Notification method invalid',
                        exception=str(e)
                    )
                )
                # No more add to log
                # Stopping the process
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
        update_history = TrackingUpdateHistory(
            found_user=found_user,
            history=history
        )
        return stats, update_history

    def build_tracker(self, track: Tracking) -> Tuple[TrackingStats, TrackingUpdateHistory]:
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
                stats, update_history = self.build_tracker(track=track)
                # do not merge if no new tweet yet.
                if stats.count > 0:
                    update[tracking_id] = update_history

        if len(list(update.keys())) > 0:
            # merging only changed and active trackings
            UserCRUD(doc_id=self.user.id).merge_tracking(
                tracking=TrackingUpdate(trackings=update)
            )
            print(f'{color.OKGREEN}Document changed <{self.user.id}>{color.END}')

    def run(self):
        self.process()
