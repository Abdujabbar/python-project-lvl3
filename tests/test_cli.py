import pytest
from page_loader.cli import get_cmd_args


def test_cmd_parse_empty():
    with pytest.raises(SystemExit):
        get_cmd_args()


@pytest.mark.parametrize(
    "url, output",
    [
        (
            "https://ru.hexlet.io/teams",
            "/var/tmp"
        ),
        (
            "https://test.com",
            "/var/tmp"
        ),
    ]
)
def test_cmd_parse_valid(url, output):
    args = get_cmd_args([url, f'-o={output}'])

    assert args.url == url
    assert args.output == output
