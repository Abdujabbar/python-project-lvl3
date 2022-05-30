import pytest
from page_loader.assets import generate_assets_path
from page_loader.html import generate_html_path


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
def test_generate_html_path(tmpdir, test_case, expected):
    assert generate_html_path(tmpdir, test_case) == f"{tmpdir}/{expected}"


@pytest.mark.parametrize(
    "test_case, expected",
    [
        (
            "https://ru.hexlet.io/teams",
            "ru-hexlet-io-teams_files"
        ),
        (
            "https://ru.hexlet.io/courses",
            "ru-hexlet-io-courses_files"
        ),
        (
            "https://pythonist.ru/chto-vy-znaete-o-list-dict-comprehensions/",
            "pythonist-ru-chto-vy-znaete-o-list-dict-comprehensions_files"
        )
    ]
)
def test_generate_generate_media_path(tmpdir, test_case, expected):
    assert generate_assets_path(tmpdir, test_case) == f"{tmpdir}/{expected}"
