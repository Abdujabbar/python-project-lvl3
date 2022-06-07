from urllib.parse import urlparse
import pytest
import os
from bs4 import BeautifulSoup
import requests_mock
from page_loader.page import download
from page_loader.assets import download_assets, get_asset_tags, prepare_assets
from page_loader.assets import ASSETS_TAGS_MAP
from tests import FIXTURES_PATH


ASSETS = [
    (
        '/blog/about',
        f"{FIXTURES_PATH}/style.css"
    ),
    (
        '/assets/application.css',
        f"{FIXTURES_PATH}/style.css"
    ),
    (
        '/assets/professions/nodejs.png',
        f"{FIXTURES_PATH}/logo.png"
    ),
    (
        '/packs/js/runtime.js',
        f"{FIXTURES_PATH}/script.js"
    ),
    (
        '/assets/professions/random-image.jpg',
        f"{FIXTURES_PATH}/random-image.jpeg"
    )
]


@pytest.mark.parametrize(
    "test_case, mock_html_path",
    [
        (
            "https://test.com",
            f"{FIXTURES_PATH}/page-with-assets.html"
        ),
    ]
)
def test_download(tmpdir, test_case, mock_html_path):
    with requests_mock.Mocker(real_http=True) as mock_request:
        with open(mock_html_path, 'r') as ctx:
            mock_request.get(test_case, text=ctx.read())

            for url, path in ASSETS:
                with open(path, "rb") as assets_context:
                    mock_request.get(
                        f"{test_case}{url}",
                        content=assets_context.read()
                    )

            output_path = download(test_case, str(tmpdir))
            assert os.path.exists(output_path)


@pytest.mark.parametrize(
    "test_case, path",
    [
        (
            "http://localhost:9000/help",
            "/var/tmp"
        )
    ]
)
def test_download_failure(test_case, path):
    with pytest.raises(Exception):
        download(test_case, path)


@pytest.mark.parametrize(
    "test_case, mock_html_path",
    [
        (
            "https://ru.hexlet.io/teams",
            f"{FIXTURES_PATH}/page-with-assets.html"
        ),
    ]
)
def test_download_assets(tmpdir, test_case, mock_html_path):
    with requests_mock.Mocker(real_http=True) as mock_request:
        with open(mock_html_path, 'r') as ctx:
            mock_request.get(test_case, text=ctx.read())

            for url, path in ASSETS:
                with open(path, "rb") as assets_context:
                    parsed_url = urlparse(test_case)
                    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

                    mock_request.get(
                        f"{domain}{url}",
                        content=assets_context.read()
                    )

            html, assets = prepare_assets(test_case, str(tmpdir))
            download_assets(assets)

            page = BeautifulSoup(html, 'html.parser')

            for tag in get_asset_tags(page):
                attr = ASSETS_TAGS_MAP[tag.name]
                asset_path = f"{str(tmpdir)}/{tag[attr]}"
                assert os.path.exists(asset_path), \
                       f"File not found: {tag[attr]}"
