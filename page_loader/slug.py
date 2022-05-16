def exclude_ext_from_path(url):
    url_parts = url.split('/')[-1].split('.')

    if len(url_parts) > 1:
        url = url_parts[-1]

    return url


def sluggify(url):
    url = url.replace('https://', '').replace('http://', '')

    result = ['-' if not c.isalpha() else c for c in url]

    return ''.join(result).strip("-")
