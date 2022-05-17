def sluggify(url):
    url = url.replace('https://', '').replace('http://', '')

    result = ['-' if not c.isalpha() else c for c in url]

    return ''.join(result).strip("-")
