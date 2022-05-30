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


def generate_assets_path(dir_path, url, suffix="_files"):
    return f"{dir_path}/{to_dir(url)}{suffix}"


def is_locale_asset(url, domain):
    obj = urlparse(url)

    return url.startswith(domain) or obj.scheme == ''


def prepare_assets(url, store_path):

    response = requests.get(url, timeout=1)

    response.raise_for_status()

    html = response.content

    logging.info(f"url: {url}, fetched content: {html}")

    parsed_url = urlparse(url)

    full_assets_path = generate_assets_path(store_path, url)

    assets = []

    logging.info(f"generated assets path: {full_assets_path}")

    soup = BeautifulSoup(html, 'html.parser')

    if not os.path.exists(full_assets_path):
        logging.info(
            f"directory not exists: {full_assets_path}, creatig . . . ")
        os.mkdir(full_assets_path)

    base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

    logging.info(f"Extracted domain: {base_domain}")

    for tag, attr in ASSETS_TAGS_MAP.items():
        found_tags = soup.find_all(tag)
        logging.info(f"Tag: {tag}, found items: {len(found_tags)}")

        for node in found_tags:
            if not node.has_attr(attr) or \
               not is_locale_asset(node[attr], base_domain):
                continue

            asset_src = node[attr]

            if not asset_src.startswith(base_domain):
                asset_src = f"{base_domain}{node[attr]}".strip()

            file_path = f"{full_assets_path}/{to_file(asset_src)}"

            node[attr] = file_path.replace(store_path, '').strip('/')

            assets.append((asset_src, file_path))

    return soup.prettify(), assets


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
