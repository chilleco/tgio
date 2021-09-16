PYTHON := env/bin/python

setup:
	python3 -m venv env
	$(PYTHON) -m pip install -r requirements.txt
