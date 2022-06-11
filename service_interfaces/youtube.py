import logging

import requests

logger = logging.getLogger(__name__)

# To fetch the data from youtube API based on params
def get_youtube_searches(params: dict):
    search_url = "https://www.googleapis.com/youtube/v3/search"

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

    else:
        return {
            "status": "fail",
            "message": "Error code: %s" % response.status_code,
            "data": response.content,
        }
