import pytest
import os
from page_loader.file import generate_html_path, generate_media_path


@pytest.mark.parametrize(
    "test_case, expected",
    [
        (
            "https://ru.hexlet.io/teams",
            f"{os.getcwd()}/ru-hexlet-io-teams.html"
        ),
        (
            "https://ru.hexlet.io/courses",
            f"{os.getcwd()}/ru-hexlet-io-courses.html"
        ),
        (
            "https://pythonist.ru/chto-vy-znaete-o-list-dict-comprehensions/",
            (
                f"{os.getcwd()}/"
                f"pythonist-ru-chto-vy-znaete-o-list-dict-comprehensions.html"
            )
        )
    ]
)
def test_generate_html_path(test_case, expected):
    assert generate_html_path(test_case) == expected


@pytest.mark.parametrize(
    "test_case, expected",
    [
        (
            "https://ru.hexlet.io/teams",
            f"{os.getcwd()}/ru-hexlet-io-teams_files"
        ),
        (
            "https://ru.hexlet.io/courses",
            f"{os.getcwd()}/ru-hexlet-io-courses_files"
        ),
        (
            "https://pythonist.ru/chto-vy-znaete-o-list-dict-comprehensions/",
            (
                f"{os.getcwd()}/"
                f"pythonist-ru-chto-vy-znaete-o-list-dict-comprehensions_files"
            )
        )
    ]
)
def test_generate_generate_media_path(test_case, expected):
    assert generate_media_path(test_case) == expected
