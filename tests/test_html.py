import pytest
import os
import vcr

from page_loader.exceptions import FailureFetchContentException
from page_loader.html import download
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
def test_download(test_case, path):

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
