install:
	poetry install

lint:
	poetry run flake8 gendiff

selfcheck:
	poetry check

check: selfcheck lint test

build: check
	poetry build

help:
	poetry run gendiff --help

test:
	poetry run pytest

package-install:
	pipx install ./dist/*.whl

package-uninstall:
	pipx uninstall hexlet-code

.PHONY: install test lint selfcheck check build help