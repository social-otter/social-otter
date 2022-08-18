from typing import List, Tuple
from datetime import datetime, timedelta
import snscrape.modules.twitter as tw

from models.social import Tweet
from models.tracking import Tracking
from models.twitter_user import TwitterUser
from models.tracking_failure_log import TrackingFailureLog


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

    def grab_new_tweets(self) -> List[Tweet]:
        seen_tweets = []
        new_tweets = []
        self.tracking.keyword = self.tracking.keyword.replace('@', '').replace('#', '')

        for search in self.search_options():
            search_str = None

            if self.tracking.misc and self.tracking.misc.last_tweet_id > 0:
                search_str = f'{search}{self.tracking.keyword} since_id:{self.tracking.misc.last_tweet_id}'
            else:
                # get tweets only during the day if it works first time
                search_str = f'{search}{self.tracking.keyword} within_time:1h'

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
            
            # print(f'Tracking tweets as {color.OKCYAN}{self.tracking.keyword}{color.END} SearchKey {color.HEADER}{search_str} {color.OKGREEN} New Tweets: {len(_tweets)} {color.WARNING} LatestSeenAt: {friendly_datetime(self.tracking.last_seen_at)}{color.END}')  # noqa

        # send the last one tweet if never sent
        if not self.tracking.misc and len(new_tweets) > 0:
            last_one = sorted(new_tweets, key=lambda x: x.id)[-1]
            return [last_one]

        return new_tweets

    def get_user(self) -> dict:
        try:
            keyword = self.tracking.keyword.replace('@', '').replace('#', '')
            results = tw.TwitterUserScraper(keyword)._get_entity()

            if isinstance(results, tw.User):
                return TwitterUser(**results.__dict__).dict()

            raise ValueError('No user found!')
        except Exception as e:
            self.tracking.failure_log.append(
                TrackingFailureLog(
                    level='critical',
                    description=f'[{self.tracking.keyword}] user not found!',
                    exception=str(e)
                )
            )
