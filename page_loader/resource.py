import logging
import requests

from page_loader.exceptions import FailureFetchContentException


def get_content(url):
    try:
        logging.info(f"Trying to connect: {url}")
        response = requests.get(url, timeout=1)
        if response.ok:
            return response.content
    except Exception as ex:
        raise FailureFetchContentException(ex)
