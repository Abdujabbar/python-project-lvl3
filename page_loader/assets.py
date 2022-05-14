import os
from bs4 import BeautifulSoup
from validators.url import url as url_validator
from page_loader.resource import get_content
from page_loader.file import save_content


def download_images(content, path):
    soup = BeautifulSoup(content, 'html.parser')

    if not os.path.exists(path):
        os.mkdir(path)

    for img in soup.find_all('img'):
        if not url_validator(img['src']):
            continue

        content = get_content(img['src'])
        file_name = img['src'].split('/')[-1]

        full_path = f"{path}/{file_name}"

        save_content(full_path, content)
        img['src'] = full_path

    return soup.prettify()


def download_assets(content, path):
    content = download_images(content, path)

    return content
