import snscrape.modules.twitter as tw
from pprint import pprint


def find_user():
    results = tw.TwitterUserScraper('elonmusk')._get_entity()
    if isinstance(results, tw.User):
        pprint(results.__dict__, indent=4)


find_user()
