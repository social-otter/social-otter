from time import time
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
        modified = False
        trackings = []

        for track in self.user.trackings:
            if track.active:
                start_time = time()
                tweets = Twitter(tracking=track).grab_tweets()
                track.elapsed_ms = round(time()-start_time, 3)
                track.last_seen_at = max([i.tweet_at for i in tweets], default=0)
                for tweet in tweets:
                    modified = True if not modified else False
                    if track.webhooks.app == 'slack':
                        slack(
                            webhook_url=track.webhooks.url,
                            tweet=tweet
                        )
            trackings.append(track)

        self.user.trackings = trackings

        if modified:
            print(f'Document changed {color.OKGREEN}<{self.user.full_name}>{color.END}')
            UserCRUD(doc_id=self.user.id).set_user_doc(self.user.dict())

    def run(self):
        self.__process()
