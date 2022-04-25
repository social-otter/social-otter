from typing import List
from datetime import datetime
import snscrape.modules.twitter as tw

from models.social import Tweet
from models.user import Tracking


class Twitter:
    def __init__(self, tracking: Tracking) -> None:
        self.tracking = tracking
        print(f'Tracking tweets for: @{self.tracking.account}')

    def search_options(self):
        search_list = []

        if self.tracking.trigger.post_from_this:
            search_list.append('from:')
        
        if self.tracking.trigger.post_to_this_by_hashtag:
            search_list.append('#')

        if self.tracking.trigger.post_to_this_by_mention:
            search_list.append('@')
        
        return search_list

    def grab_tweets(self) -> List[Tweet]:
        print('Grabbing tweets...')
        _seen, _tweets = [], []
        today = datetime.now().strftime('%Y-%m-%d')

        for search in self.search_options():
            search_str = f'{search}{self.tracking.account} since:{today}'
            results = tw.TwitterSearchScraper(search_str).get_items()
            data = list(results)
            print(f'Search Option: {search} found tweet count: {len(data)}')

            for x in data:
                tweet_at = int(datetime.timestamp(x.date))

                if x.id not in _seen and tweet_at > self.tracking.last_seen_at:
                    print(f'Adding to list {x.url}')
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

        # send the last one tweet if never sent
        if self.tracking.last_seen_at == 0 and len(_tweets) > 1:
            last_one = sorted(_tweets, key=lambda x: x.tweet_at)[-1]
            return [last_one]

        return _tweets
