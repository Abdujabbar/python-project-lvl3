import requests_mock
import pytest
import subprocess
from tests import FIXTURES_PATH


def capture(command):
    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    out, err = proc.communicate()
    return out, err, proc.returncode


@pytest.mark.parametrize(
    "url, output, expected_code, path",
    [
        (
            "https://ru.hexlet.io/teams",
            "/var/tmp",
            0,
            f"{FIXTURES_PATH}/page-with-assets.html"
        ),
        (
            "https://ru.hexlet.io",
            "/var/tmp",
            0,
            f"{FIXTURES_PATH}/page-with-assets.html"
        ),
    ]
)
def test_cmd_parse_valid(url, output, expected_code, path):
    with requests_mock.Mocker(real_http=True) as mock_request:
        with open(path, 'r') as ctx:
            mock_request.get(url, text=ctx.read())
            command = ["poetry", "run", "page-loader", url, f"-o={output}"]
            out, err, exitcode = capture(command)
            print(out, err)
            assert exitcode == expected_code, "Trouble while execute"


@pytest.mark.parametrize(
    "url, output, expected_code",
    [
        (
            "https://localhost:1233",
            "/var/tmp",
            1
        ),
        (
            "https://test.com",
            "/var/tmp",
            1
        ),
    ]
)
def test_cmd_exception(url, output, expected_code):
    command = ["poetry", "run", "page-loader", url, f"-o={output}"]
    _, _, exitcode = capture(command)
    assert exitcode == expected_code, "Trouble while execute"
