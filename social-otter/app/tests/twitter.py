import snscrape.modules.twitter as tw
from rich.console import Console

console = Console()


def find_user():
    results = tw.TwitterUserScraper('elonmusk')._get_entity()
    if isinstance(results, tw.User):
        console.print(results.__dict__)


find_user()
