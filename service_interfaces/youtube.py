import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def get_youtube_searches(date, search_param: str):
    search_url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": search_param,
        "key": settings.YOUTUBE_DATA_API_KEY,
        "type": "video",
        "order": "date",
        "publishedAfter": date,
    }

    session = requests.Session()
    try:
        response = session.get(search_url, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Error while getting youtube search: {e}")
        return {
            "status": "fail",
            "message": "Can't connect!",
            "data": {},
        }

    if response.ok:
        return {
            "status": "success",
            "message": "data received",
            "data": response.json(),
        }
