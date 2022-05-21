import logging
from page_loader.storage import generate_html_path
from page_loader.storage import save_content
from page_loader.assets import prepare_assets, download_assets


def download(url, dir_path):
    logging.info(f"url: {url}, dir_path: {dir_path}")

    html, assets = prepare_assets(url, dir_path)

    download_assets(assets)

    html_path = generate_html_path(url, dir_path)

    logging.info(f"html_path: {html_path}")

    save_content(html_path, html.encode())

    return html_path
