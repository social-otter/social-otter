import threading
from storage.user import UserCRUD
from integrations.twitter import Twitter
from models.user import User
from channels.slack import slack


class Worker(threading.Thread):
    def __init__(self, user: User) -> None:
        threading.Thread.__init__(self)
        self.user = user
        print(f'Worker started for <{self.user.full_name}>')

    def _process(self):
        modified = False
        trackings = []

        for track in self.user.trackings:
            tweets = Twitter(tracking=track).grab_tweets()
            track.last_seen_at = max([i.tweet_at for i in tweets], default=0)
            trackings.append(track)

            for tweet in tweets:
                modified = True if not modified else False
                if track.webhooks.app == 'slack':
                    slack(
                        webhook_url=track.webhooks.url,
                        tweet=tweet
                    )

        self.user.trackings = trackings

        if modified:
            print(f'Document changed <{self.user.full_name}>')
            UserCRUD(doc_id=self.user.id).set_user_doc(self.user.dict())

    def run(self):
        self._process()
