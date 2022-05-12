import pytest
from page_loader.slug import sluggify


@pytest.mark.parametrize(
    "test_case, expected",
    [
        (
            "https://ru.hexlet.io/teams",
            "ru-hexlet-io-teams"
        ),
        (
            "https://ru.hexlet.io/courses",
            "ru-hexlet-io-courses"
        ),
        (
            "https://pythonist.ru/chto-vy-znaete-o-list-dict-comprehensions/",
            "pythonist-ru-chto-vy-znaete-o-list-dict-comprehensions"
        )
    ]
)
def test_sluggify(test_case, expected):
    assert sluggify(test_case) == expected
