import os
from urllib.parse import urlparse


def to_dir(url):
    url = url.strip('/')
    parsed_url = urlparse(url)

    url = f"{parsed_url.netloc}{parsed_url.path}"

    result = ['-' if not c.isalnum() else c for c in url]

    return f"{''.join(result)}"


def to_file(url, default_ext='.html'):
    url = url.strip('/')
    parsed_url = urlparse(url)

    ext = os.path.splitext(parsed_url.path)[1]

    url = url.replace('https://', '').replace('http://', '').replace(ext, '')

    result = ['-' if not c.isalnum() else c for c in url]

    return f"{''.join(result)}{ext or default_ext}"
