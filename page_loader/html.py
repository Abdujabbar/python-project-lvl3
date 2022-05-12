from page_loader.file import generate_html_path
from page_loader.file import generate_media_path
from page_loader.file import save_content
from page_loader.media import download_images
from page_loader.page import get_content


def download(url, dir_path):
    content = get_content(url)

    media_path = generate_media_path(url, dir_path)

    content = download_images(content, media_path)

    html_path = generate_html_path(url, dir_path)

    save_content(html_path, content.encode())

    return html_path
