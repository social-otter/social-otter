from typing import List, Tuple
from datetime import datetime, timedelta
import snscrape.modules.twitter as tw

from models.social import Tweet
from models.tracking import Tracking
from models.twitter_user import TwitterUser

# from utils.termcolors import color
# from utils.dateops import friendly_datetime


class Twitter:
    def __init__(self, tracking: Tracking) -> None:
        self.tracking = tracking

    def search_options(self):
        search_list = []

        if self.tracking.trigger.post_from_this:
            search_list.append('from:')
        
        if self.tracking.trigger.post_to_this_by_hashtag:
            search_list.append('#')

        if self.tracking.trigger.post_to_this_by_mention:
            search_list.append('@')
        
        return search_list

    def grab_new_tweets(self) -> Tuple[int, List[Tweet]]:
        since = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        _seen = []
        _tweets = []
        tweet_counts = 0

        for search in self.search_options():
            keyword = self.tracking.account.replace('@', '').replace('#', '')
            search_str = f'{search}{keyword} since:{since}'
            results = tw.TwitterSearchScraper(search_str).get_items()
            data = list(results)
            tweet_counts += len(data)

            for x in data:
                tweet_at = datetime.timestamp(x.date)

                if x.id not in _seen and tweet_at > self.tracking.last_seen_at:
                    tweet = Tweet(
                        id=x.id,
                        content=x.content,
                        url=x.url,
                        date=x.date.strftime("%H:%M:%S %m/%d/%Y"),
                        username=x.user.username,
                        displayname=x.user.displayname,
                        profileImageUrl=x.user.profileImageUrl,
                        tweet_at=tweet_at
                    )
                    _tweets.append(tweet)
                    _seen.append(tweet.id)
            
            # print(f'Tracking tweets as {color.OKCYAN}{self.tracking.account}{color.END} SearchKey {color.HEADER}{search_str} {color.OKGREEN} New Tweets: {len(_tweets)} {color.WARNING} LatestSeenAt: {friendly_datetime(self.tracking.last_seen_at)}{color.END}')  # noqa

        # send the last one tweet if never sent
        if self.tracking.last_seen_at == 0 and len(_tweets) > 1:
            last_one = sorted(_tweets, key=lambda x: x.tweet_at)[-1]
            return tweet_counts, [last_one]

        return tweet_counts, _tweets

    def get_user(self) -> dict:
        try:
            keyword = self.tracking.account.replace('@', '').replace('#', '')
            results = tw.TwitterUserScraper(keyword)._get_entity()

            if isinstance(results, tw.User):
                return TwitterUser(**results.__dict__).dict()
        except:
            ...
