import os
from page_loader.slug import sluggify


def generate_media_path(url, dir_path=os.getcwd()):
    return f"{dir_path}/{sluggify(url)}_files"


def generate_html_path(url, dir_path=os.getcwd()):
    return f"{dir_path}/{sluggify(url)}.html"


def save_content(path, content):
    with open(path, 'wb') as ctx:
        ctx.write(content)
