PYTHON := env/bin/python

setup:
	python3 -m venv env
	$(PYTHON) -m pip install -r requirements.txt

setup-tests:
	make setup
	$(PYTHON) -m pip install -r tests/requirements.txt

setup-release:
	python3 -m venv env
	$(PYTHON) -m pip install -r requirements.dev.txt

setup-all:
	make setup-tests
	make setup-release

test-lint-all:
	find . -type f -name '*.py' \
	| grep -vE 'env/' \
	| grep -vE 'tests/' \
	| grep -vE 'build/' \
	| xargs $(PYTHON) -m pylint -f text \
		--rcfile=tests/.pylintrc \
		--msg-template='{path}:{line}:{column}: [{symbol}] {msg}'

test-lint:
	git status -s \
	| grep -vE 'tests/' \
	| grep '\.py$$' \
	| awk '{print $$1,$$2}' \
	| grep -i '^[ma]' \
	| awk '{print $$2}' \
	| xargs $(PYTHON) -m pylint -f text \
		--rcfile=tests/.pylintrc \
		--msg-template='{path}:{line}:{column}: [{symbol}] {msg}'

test-unit-all:
	$(PYTHON) -m pytest -s tests/

test-unit:
	git status -s \
	| grep 'tests/.*\.py$$' \
	| awk '{print $$1,$$2}' \
	| grep -i '^[ma]' \
	| awk '{print $$2}' \
	| xargs $(PYTHON) -m pytest -s

test:
	make test-lint-all
	make test-unit-all

release:
	make clean
	$(PYTHON) setup.py sdist bdist_wheel
	sudo $(PYTHON) -m twine upload dist/*

clean:
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

clear:
	rm -rf env/
	rm -rf **/env/
	rm -rf __pycache__/
	rm -rf **/__pycache__/
	rm -rf .pytest_cache/
	rm -rf **/.pytest_cache/
