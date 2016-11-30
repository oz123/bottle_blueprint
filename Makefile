.PHONY: test flush clean_all clean clean_docs clean_coverage_report clean-build clean-pyc

help:
	@echo "run - run the development server"
	@echo "clean - clean-build + clean-pyc"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "flush - ** DANGER ** erase everything not in git"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"

run:
	python main.py

test:
	pytest -vv

flush:
	git clean -x -d -f


clean_all: clean clean_docs clean_coverage_report


clean: clean-build clean-pyc


clean_docs:
	$(MAKE) -C docs clean


clean_coverage_report:
	rm -rf htmlcov/


clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

coverage-run:
	coverage run -m py.test

coverage: coverage-run
