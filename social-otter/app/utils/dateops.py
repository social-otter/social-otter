
from datetime import datetime


def friendly_datetime(timestamp: float):
    try:
        return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return None
