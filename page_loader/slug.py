
def sluggify(url):
    url = url.replace('https://', '').replace('http://', '')

    result = []

    for c in url:
        if not c.isalpha():
            result.append('-')
        else:
            result.append(c)

    return ''.join(result).strip("-")
