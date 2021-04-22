install:
	poetry install

lint:
	poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck lint test

build: check
	poetry build

help:
	poetry run page_loader --help

test:
	PYTHONPATH=. poetry run  pytest

package-install:
	pipx install ./dist/*.whl

package-uninstall:
	pipx uninstall hexlet-code

black:
	black . --skip-string-normalization

.PHONY: install test lint selfcheck check build help formatted