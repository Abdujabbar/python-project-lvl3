from page_loader.media import download_images
from page_loader.page import get_content
import vcr
import pytest
import os
from bs4 import BeautifulSoup
from tests import FIXTURES_PATH


@vcr.use_cassette(f"{FIXTURES_PATH}/cassettes/test_download")
@pytest.mark.parametrize(
    "test_case, path",
    [
        (
            "https://ru.hexlet.io/teams",
            "/var/tmp",
        ),
    ]
)
def test_download_images(test_case, path):
    content = get_content(test_case)

    content = download_images(content, path)

    soup = BeautifulSoup(content, 'html.parser')

    for img in soup.find_all('img'):
        assert os.path.exists(img['src']), "File doesn't exists: {img['src']}"
