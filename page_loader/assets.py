import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from page_loader.resource import get_content
from page_loader.storage import generate_assets_path, save_content


ASSETS_WITH_SRC_MAP = {
    'link': 'href',
    'img': 'src',
    'script': 'src'
}


def generate_public_path(media_path, store_path):
    return media_path.replace(store_path, '').strip('/')


def is_locale_resource(url):
    obj = urlparse(url)

    return obj.scheme == ''


def extract_source_name(url):
    obj = urlparse(url)

    return obj.path.split('/')[-1]


def extract_domain_with_protocol(url):
    obj = urlparse(url)

    return url.replace(obj.path, '')


def download_assets(url, store_path):
    html = get_content(url)

    assets_path = generate_assets_path(url, store_path)

    soup = BeautifulSoup(html, 'html.parser')

    if not os.path.exists(assets_path):
        os.mkdir(assets_path)

    domain = extract_domain_with_protocol(url)

    for tag, attr in ASSETS_WITH_SRC_MAP.items():
        for node in soup.find_all(tag):
            if not node.has_attr(attr) or not is_locale_resource(node[attr]):
                continue

            asset_src = f"{domain}{node[attr]}".strip()
            content = get_content(asset_src)

            if not content:
                continue

            file_name = extract_source_name(asset_src)
            full_image_path = f"{assets_path}/{file_name}"
            save_content(full_image_path, content)

            node[attr] = generate_public_path(full_image_path, store_path)

    return soup.prettify()
