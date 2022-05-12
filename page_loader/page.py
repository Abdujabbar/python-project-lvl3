import requests

from page_loader.exceptions import FailureFetchContentException


def get_content(url):
    try:
        response = requests.get(url)

        if response.ok:
            return response.content
    except Exception as ex:
        raise FailureFetchContentException(ex)