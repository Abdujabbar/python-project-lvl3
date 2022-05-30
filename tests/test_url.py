import pytest
from page_loader.url import to_file


@pytest.mark.parametrize(
    "test_case, expected",
    [
        (
            "https://ru.hexlet.io/teams",
            "ru-hexlet-io-teams.html"
        ),
        (
            "https://ru.hexlet.io/courses",
            "ru-hexlet-io-courses.html"
        ),
        (
            "https://pythonist.ru/chto-vy-znaete-o-list-dict-comprehensions/",
            "pythonist-ru-chto-vy-znaete-o-list-dict-comprehensions.html"
        )
    ]
)
def test_sluggify(test_case, expected):
    assert to_file(test_case) == expected
