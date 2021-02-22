install:
		poetry install
build:
		poetry build

publish:
		poetry publish --dry-run

package-install:
		pip install --user dist/*.whl

lint:
		poetry run flake8 page_loader
		poetry run flake8 tests

pytest:
		poetry run pytest --cov=page_loader tests/ --cov-report xml