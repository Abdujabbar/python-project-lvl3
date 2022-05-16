from page_loader.storage import generate_html_path
from page_loader.storage import save_content
from page_loader.assets import download_assets


def download(url, dir_path):
    content = download_assets(url, dir_path)

    html_path = generate_html_path(url, dir_path)

    save_content(html_path, content.encode())

    return html_path
