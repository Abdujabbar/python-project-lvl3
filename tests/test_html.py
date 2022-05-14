import pytest
import os
import requests_mock
from page_loader.exceptions import FailureFetchContentException
from page_loader.html import download
from tests import FIXTURES_PATH


@pytest.mark.parametrize(
    "test_case, path, mock_html_path",
    [
        (
            "https://ru.hexlet.io/teams",
            "/var/tmp",
            f"{FIXTURES_PATH}/page-with-assets.html"
        ),
    ]
)
def test_download(test_case, path, mock_html_path):
    with requests_mock.Mocker() as mock_request:
        with open(mock_html_path, 'r') as ctx:
            mock_request.get(test_case, ctx.read())

            output_path = download(test_case, path)

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
