import os
import requests
import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from page_loader.url import to_dir, to_file
from progress.bar import IncrementalBar
from concurrent import futures


ASSETS_TAGS_MAP = {
    'link': 'href',
    'img': 'src',
    'script': 'src'
}


def get_asset_tags(page: BeautifulSoup):
    tags = []
    for tag in ASSETS_TAGS_MAP.keys():
        tags.extend(page(tag))

    return tags


def generate_assets_path(dir_path, url, suffix="_files"):
    return f"{dir_path}/{to_dir(url)}{suffix}"


def prepare_assets(url, store_path):

    response = requests.get(url, timeout=1)

    response.raise_for_status()

    html = response.content

    logging.info(f"url: {url}, fetched content: {html}")

    parsed_url = urlparse(url)

    full_assets_path = generate_assets_path(store_path, url)

    logging.info(f"generated assets path: {full_assets_path}")

    page = BeautifulSoup(html, 'html.parser')

    if not os.path.exists(full_assets_path):
        logging.info(
            f"directory not exists: {full_assets_path}, creatig . . . ")
        os.mkdir(full_assets_path)

    assets = []

    base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

    logging.info(f"Extracted domain: {base_domain}")

    for tag in get_asset_tags(page):
        attr = ASSETS_TAGS_MAP[tag.name]
        asset_src = tag[attr]
        parsed_asset_url = urlparse(asset_src)

        if parsed_asset_url.netloc and\
           parsed_url.netloc != parsed_asset_url.netloc:
            continue

        if not parsed_asset_url.netloc:
            asset_src = f"{base_domain}{parsed_asset_url.path}".strip()

        file_path = f"{full_assets_path}/{to_file(asset_src)}"

        tag[attr] = file_path.replace(store_path, '').strip('/')

        assets.append((asset_src, file_path))

    return page.prettify(), assets


def download_assets(assets):
    if not assets:
        return

    bar_width = len(assets)

    bar = IncrementalBar("Downloading:", max=bar_width)
    with futures.ThreadPoolExecutor(max_workers=8) as executor, bar:
        tasks = [
            executor.submit(download_asset, url, path, bar)
            for url, path in assets
        ]
        result = [task.result() for task in tasks]
        logging.info(f"All assets was downloaded: {result}")


def download_asset(url, path, bar):
    logging.info(f"Trying to download asset: {url}"
                 f"Path for save: {path}")

    try:
        response = requests.get(url, timeout=1)
        response.raise_for_status()

        with open(path, 'wb') as ctx:
            ctx.write(response.content)

        bar.next()

        return path
    except Exception as ex:
        cause_info = (ex.__class__, ex, ex.__traceback__)
        logging.debug(str(ex), exc_info=cause_info)
        logging.warning(
            f"Resource {url} wasn't downloaded"
        )
