import os
from urllib.parse import urlparse


def sluggify(url, default_ext='.html'):
    url = url.strip('/')

    parsed_url = urlparse(url)

    ext = os.path.splitext(parsed_url.path)[1]

    if not ext:
        ext = default_ext

    url = url.replace('http://', '').replace('https://', '').replace(ext, '')

    result = ['-' if not c.isalpha() else c for c in url]

    return f"{''.join(result)}{ext}"
