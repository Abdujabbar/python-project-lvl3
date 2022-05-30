import logging
from page_loader.assets import prepare_assets, download_assets
from page_loader.url import to_file


def generate_html_path(base_dir, url):
    return f"{base_dir}/{to_file(url, '.html')}"


def download(url, dir_path):
    logging.info(f"url: {url}, dir_path: {dir_path}")

    html, assets = prepare_assets(url, dir_path)
    html_path = f"{dir_path}/{to_file(url, '.html')}"

    logging.info(f"generated assets: {assets}")
    download_assets(assets)

    logging.info(f"Downloading html_path: {html_path} for url: {url}")

    with open(html_path, 'w') as ctx:
        ctx.write(html)

    logging.info("Finish download")

    return html_path
