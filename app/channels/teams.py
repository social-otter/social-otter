import requests


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
