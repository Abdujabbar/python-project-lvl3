import logging
from page_loader.storage import generate_html_path
from page_loader.assets import prepare_assets, download_assets


def download(url, dir_path):
    logging.info(f"url: {url}, dir_path: {dir_path}")

    html, assets = prepare_assets(url, dir_path)
    html_path = generate_html_path(url, dir_path)

    download_assets(assets)

    logging.info(f"Downloading html_path: {html_path} for url: {url}")

    with open(html_path, 'w') as ctx:
        ctx.write(html)

    logging.info("Finish download")

    return html_path
