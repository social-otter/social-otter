from time import time
from typing import List, Tuple
import snscrape.modules.twitter as tw

from models.social import Tweet
from models.tracking import Tracking
from models.twitter_user import TwitterUser
from models.tracking_stats import TrackingStats
from models.tracking_failure_log import TrackingFailureLog


class Twitter:
    def __init__(self, tracking: Tracking) -> None:
        self.tracking = tracking
        self.init_safe_keyword()
        self.errors = []

    def init_safe_keyword(self):
        self.keyword = self.tracking.keyword.replace('@', '').replace('#', '')

    def search_options(self):
        search_list = []

        if self.tracking.trigger.post_from_this:
            search_list.append(('from:', 'new_post'))

        if self.tracking.trigger.post_to_this_by_hashtag:
            search_list.append(('#', 'hashtag'))

        if self.tracking.trigger.post_to_this_by_mention:
            search_list.append(('@', 'mention'))

        return search_list

    def grab_new_tweets(self) -> Tuple[TrackingStats, List[Tweet]]:
        t0 = time()
        seen_tweets = []
        new_tweets = []
        last_tweet_id = 0
        detail = {}

        if self.tracking.history:
            if self.tracking.history.misc:
                last_tweet_id = self.tracking.history.misc.last_tweet_id

        for option in self.search_options():
            search, search_type = option
            tweet_counts = 0
            search_str = None

            if last_tweet_id > 0:
                search_str = f'{search}{self.keyword} since_id:{self.tracking.history.misc.last_tweet_id}'  # noqa
            else:
                # get tweets only during the day if it works first time
                search_str = f'{search}{self.keyword} within_time:1h'

            results = tw.TwitterSearchScraper(search_str).get_items()
            data = list(results)

            for x in data:
                x: tw.Tweet = x
                if x.id not in seen_tweets:
                    tweet = Tweet(
                        id=x.id,
                        content=x.content,
                        url=x.url,
                        date=x.date.strftime("%H:%M:%S %m/%d/%Y"),
                        username=x.user.username,
                        displayname=x.user.displayname,
                        profileImageUrl=x.user.profileImageUrl,
                    )
                    new_tweets.append(tweet)
                    seen_tweets.append(tweet.id)
                    tweet_counts += 1

            detail[search_type] = tweet_counts

        stats = TrackingStats(
            timestamp=time(),
            elapsed_sec=int(time()-t0),
            count=len(new_tweets),
            detail=detail
        )

        # send the last one tweet if never sent
        if last_tweet_id == 0 and len(new_tweets) > 0:
            last_one = sorted(new_tweets, key=lambda x: x.id)[-1]
            return stats, [last_one]

        return stats, new_tweets

    def get_user(self) -> dict:
        try:
            results = tw.TwitterUserScraper(self.keyword)._get_entity()

            if isinstance(results, tw.User):
                return TwitterUser(**results.__dict__).dict()

            raise ValueError('No user found!')
        except Exception as e:
            self.errors.append(
                TrackingFailureLog(
                    level='critical',
                    description=f'[{self.keyword}] user not found!',
                    exception=str(e)
                )
            )
