import pytest
import os
from bs4 import BeautifulSoup
import requests_mock
from page_loader.exceptions import FailureFetchContentException
from page_loader.html import download
from page_loader.assets import download_assets, prepare_assets
from page_loader.assets import ASSETS_WITH_SRC_MAP
from tests import FIXTURES_PATH


@pytest.fixture
def image():
    with open(f"{FIXTURES_PATH}/logo.png", "rb") as ctx:
        yield ctx.read()


@pytest.fixture
def css():
    with open(f"{FIXTURES_PATH}/style.css", "r") as ctx:
        yield ctx.read()


@pytest.fixture
def js():
    with open(f"{FIXTURES_PATH}/script.js", "r") as ctx:
        yield ctx.read()


@pytest.mark.parametrize(
    "test_case, mock_html_path",
    [
        (
            "https://test.com",
            f"{FIXTURES_PATH}/page-with-assets.html"
        ),
    ]
)
def test_download(tmpdir, test_case, mock_html_path, image, css, js):
    with requests_mock.Mocker(real_http=True) as mock_request:
        with open(mock_html_path, 'r') as ctx:
            mock_request.get(test_case, text=ctx.read())
            mock_request.get(
                f"{test_case}/assets/professions/nodejs.png", content=image)
            mock_request.get(f"{test_case}/assets/application.css", text=css)
            mock_request.get(f"{test_case}/packs/js/runtime.js", text=js)
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
    with pytest.raises(FailureFetchContentException):
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
def test_download_assets(tmpdir, test_case, mock_html_path, image, css, js):
    with requests_mock.Mocker(real_http=True) as mock_request:
        with open(mock_html_path, 'r') as ctx:
            mock_request.get(test_case, text=ctx.read())
            mock_request.get(test_case, text=ctx.read())
            mock_request.get(
                f"{test_case}/assets/professions/nodejs.png", content=image)
            mock_request.get(f"{test_case}/assets/application.css", text=css)
            mock_request.get(f"{test_case}/packs/js/runtime.js", text=js)

            html, assets = prepare_assets(test_case, str(tmpdir))
            download_assets(assets)

            soup = BeautifulSoup(html, 'html.parser')

            for tag, attr in ASSETS_WITH_SRC_MAP.items():
                for node in soup.find_all(tag):
                    asset_path = f"{str(tmpdir)}/{node[attr]}"
                    assert os.path.exists(asset_path), \
                           f"File not found: {node[attr]}"
