.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  help\t\tPrint this help"
	@echo "  setup\t\tInstall requirements"
	@echo "  build\t\tBuild Package"
	@echo "  test\t\tRun tests"
	@echo "  publish\tPublish package to pypi"

.PHONY: test
test:
	tox

.PHONY: setup
setup:
	sudo apt-get install libpq-dev
	pip install -e .[dev]

build: setup.py src/datawarehouse.py
	python setup.py bdist_wheel sdist

.PHONY: publish
publish:
	twine upload dist/*
