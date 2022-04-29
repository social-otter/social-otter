from time import time
from datetime import datetime
from storage.user import UserCRUD
from integrations.twitter import Twitter
from models.user import User
from channels.slack import slack
from utils.termcolors import color


class Worker():
    def __init__(self, user: User) -> None:
        # threading.Thread.__init__(self)
        self.user = user
        print(f'Worker started for {color.WARNING}<{self.user.full_name}>{color.END}')

    def __process(self):
        trackings = []

        for track in self.user.trackings:
            if track.active:
                start_time = time()
                tweets = Twitter(tracking=track).grab_new_tweets()
                track.elapsed_ms = round(time()-start_time, 3)
                track.last_seen_at = max([i.tweet_at for i in tweets], default=0)
                track.last_seen_at_friendly = datetime.utcfromtimestamp(track.last_seen_at).strftime("%Y-%m-%d %H:%M:%S")
                for tweet in sorted(tweets, key=lambda x: x.tweet_at):
                    if track.webhooks.app == 'slack':
                        slack(
                            webhook_url=track.webhooks.url,
                            tweet=tweet
                        )
            trackings.append(track)

        self.user.trackings = trackings
        if len(tweets) > 0:
            UserCRUD(doc_id=self.user.id).set_user_doc(self.user.dict())
            print(f'Document changed {color.OKGREEN}<{self.user.full_name}>{color.END}')
        else:
            print(f'{color.FAIL}There are no new tweets, yet.{color.END}')

    def run(self):
        self.__process()
