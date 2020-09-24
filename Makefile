.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  help\t\tPrint this help"
	@echo "  setup\t\tInstall requirements"
	@echo "  build\t\tBuild Package"
	@echo "  test\t\tRun tests"
	@echo "  install\tInstall package in development"
	@echo "  publish\tPublish package to pypi"
	@echo "  clean\t\tRemove development files"

.PHONY: setup
setup:
	sudo apt-get install libpq-dev

build: setup.py src/uetl.py
	python setup.py bdist_wheel sdist

.PHONY: test
test:
	tox

.PHONY: install
install:
	pip install -e .[dev]

.PHONY: publish
publish:
	twine upload dist/*

.PHONY: clean
clean:
	rm -rf build/ dist/ .tox/ src/uetl.egg-info/ tests/__pycache__/
	pip uninstall -y uetl
