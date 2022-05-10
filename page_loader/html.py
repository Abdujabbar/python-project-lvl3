import requests
from page_loader.file import generate_name


def get_page_content(url):

    response = requests.get(url)

    if response.ok:
        return response.content

    raise Exception(
        f"Trouble while get content,"
        f"response status: {response.status_code}")


def download(url, dir_path):
    file_name = generate_name(url)

    path_to_store = f"{dir_path}/{file_name}"

    content = get_page_content(url)

    with open(path_to_store, 'wb') as ctx:
        ctx.write(content)
