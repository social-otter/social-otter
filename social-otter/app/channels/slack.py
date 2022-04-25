import requests
from models.social import Tweet

# Sample Zapier integration url
# https://zapier.com/app/login?next=/engine/oauth/http/redirect/SlackAPI/?
# utm_source=partner_slack_install
# utm_medium=embed_custom_zapier
# utm_campaign=slack_zapier_integration


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


def teams(webhook_url, message):
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "message",
                    "version": "1.5",
                    ""
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": message,
                            "wrap": True
                        }
                    ]

                }
            }
        ]
    }
    
    return requests.post(url=webhook_url, json=payload)
