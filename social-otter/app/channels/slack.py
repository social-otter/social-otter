import requests
from models.social import Tweet


def slack(webhook_url, tweet: Tweet):
    # https://app.slack.com/block-kit-builder/

    payload = {
        "blocks": [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": tweet.profileImageUrl,
                        "alt_text": tweet.displayname
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*{tweet.displayname}* <{tweet.url}|@{tweet.username}>"
                    },
                    {
                        "type": "mrkdwn",
                        "text": tweet.date
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": tweet.content
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": tweet.url
                }
            },
            {
                "type": "divider"
            },
        ]
    }    
    return requests.post(url=webhook_url, json=payload)
