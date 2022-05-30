import pytest
from page_loader.url import to_file


@pytest.mark.parametrize(
    "test_case, default_ext, expected",
    [
        (
            "https://ru.hexlet.io/teams",
            '.html',
            "ru-hexlet-io-teams.html"
        ),
        (
            "https://ru.hexlet.io/courses",
            '',
            "ru-hexlet-io-courses"
        ),
        (
            "https://pythonist.ru/chto-vy-znaete-o-list-dict-comprehensions/",
            '.html',
            "pythonist-ru-chto-vy-znaete-o-list-dict-comprehensions.html"
        )
    ]
)
def test_sluggify(test_case, default_ext, expected):
    assert to_file(test_case, default_ext) == expected