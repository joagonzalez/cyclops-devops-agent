run:
	API_VERSION=$$(cat VERSION) uv run python run.py

install:
	uv sync

typehint:
	uv run mypy src/ tests/

test-local:
	uv run pytest tests/ -v --cov

test:
	uv run pytest tests/ -v --cov --cov-report=xml:coverage.xml

lint:
	uv run ruff check src/ tests/ 

format:
	uv run ruff check src/ tests/ --fix

doc:
	uv run mkdocs serve

build-images:
	@echo "Implement build images"

deploy-local:
	@echo "Implement deploy within local environment"

deploy:
	@echo "Implement deploy within k8s cluster"

clean:
	rm -rf .*_cache coverage.xml .*coverage site report

checklist: typehint lint test clean

code-quality: typehint lint clean

coverage-publish:
	uv run coveralls

.PHONY: checklist