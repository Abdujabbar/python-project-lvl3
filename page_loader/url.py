import os
import re
from urllib.parse import urlparse


def to_dir(url):
    url = url.strip('/')
    parsed_url = urlparse(url)

    url = f"{parsed_url.netloc}{parsed_url.path}"

    result = re.sub(r"[^a-z0-9+]", '-', url)

    return f"{''.join(result)}"


def to_file(url, default_ext='.html'):
    url = url.strip('/')
    parsed_url = urlparse(url)

    ext = os.path.splitext(parsed_url.path)[1]

    url = f"{parsed_url.netloc}{parsed_url.path}".replace(ext, '')

    result = re.sub(r"[^a-z0-9+]", '-', url)

    return f"{result}{ext or default_ext}"
