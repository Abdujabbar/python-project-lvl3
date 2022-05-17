import os
import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from page_loader.resource import get_content
from page_loader.storage import generate_assets_path, save_content
from progress.bar import IncrementalBar
from concurrent import futures


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

    return f"{obj.scheme}://{obj.netloc}"


def prepare_assets(url, store_path):
    html = get_content(url)

    assets_path = generate_assets_path(url, store_path)

    assets = []

    logging.info(f"generated assets path: {assets_path}")

    soup = BeautifulSoup(html, 'html.parser')

    if not os.path.exists(assets_path):
        logging.info(f"directory not exists: {assets_path}, creatig . . . ")
        os.mkdir(assets_path)

    domain = extract_domain_with_protocol(url)

    logging.info(f"Extracted domain: {domain}")

    for tag, attr in ASSETS_WITH_SRC_MAP.items():
        for node in soup.find_all(tag):
            if not node.has_attr(attr) or not is_locale_resource(node[attr]):
                continue

            asset_src = f"{domain}{node[attr]}".strip()

            file_name = extract_source_name(asset_src)
            full_image_path = f"{assets_path}/{file_name}"

            node[attr] = generate_public_path(full_image_path, store_path)

            assets.append((asset_src, full_image_path))

    return soup.prettify(), assets


def download_assets(assets):
    if not assets:
        return

    bar_width = len(assets)

    global bar
    bar = IncrementalBar("Downloading:", max=bar_width)
    with futures.ThreadPoolExecutor(max_workers=8) as executor, bar:
        tasks = [
            executor.submit(download_asset, url, path, bar)
            for url, path in assets
        ]
        result = [task.result() for task in tasks]
        logging.info(f"All assets was downloaded: {result}")


def download_asset(url, path, bar):
    try:
        content = get_content(url)

        save_content(path, content)

        bar.next()

        return path
    except Exception as ex:
        cause_info = (ex.__class__, ex, ex.__traceback__)
        logging.debug(str(ex), exc_info=cause_info)
        logging.warning(
            f"Page resource {url} wasn't downloaded"
        )
