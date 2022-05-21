install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	poetry run flake8 .

page_loader:
	poetry run page_loader

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=page_loader tests/ --cov-report xml
