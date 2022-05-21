import os
import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from page_loader.resource import get_content
from page_loader.slug import sluggify
from page_loader.storage import generate_assets_path
from progress.bar import IncrementalBar
from concurrent import futures


ASSETS_WITH_SRC_MAP = {
    'link': 'href',
    'img': 'src',
    'script': 'src'
}


def generate_public_path(media_path, store_path):
    return media_path.replace(store_path, '').strip('/')


def is_valid_asset(url, domain):
    obj = urlparse(url)

    return url.startswith(domain) or obj.scheme == ''


def get_domain(url):
    obj = urlparse(url)

    return f"{obj.scheme}://{obj.netloc}"


def prepare_assets(url, store_path):

    html = get_content(url)
    logging.info(f"url: {url}, fetched content: {html}")

    assets_path = generate_assets_path(url, store_path)

    assets = []

    logging.info(f"generated assets path: {assets_path}")

    soup = BeautifulSoup(html, 'html.parser')

    if not os.path.exists(assets_path):
        logging.info(f"directory not exists: {assets_path}, creatig . . . ")
        os.mkdir(assets_path)

    base_domain = get_domain(url)

    logging.info(f"Extracted domain: {base_domain}")

    for tag, attr in ASSETS_WITH_SRC_MAP.items():
        found_tags = soup.find_all(tag)
        logging.info(f"Tag: {tag}, found items: {len(found_tags)}")

        for node in found_tags:
            if not node.has_attr(attr)\
               or not is_valid_asset(node[attr], base_domain):
                continue

            asset_src = node[attr]

            if not asset_src.startswith(base_domain):
                asset_src = f"{base_domain}{node[attr]}".strip()

            full_image_path = f"{assets_path}/{sluggify(asset_src)}"

            node[attr] = generate_public_path(full_image_path, store_path)

            assets.append((asset_src, full_image_path))

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
        content = get_content(url)

        with open(path, 'wb') as ctx:
            ctx.write(content)

        bar.next()

        return path
    except Exception as ex:
        cause_info = (ex.__class__, ex, ex.__traceback__)
        logging.debug(str(ex), exc_info=cause_info)
        logging.warning(
            f"Resource {url} wasn't downloaded"
        )
