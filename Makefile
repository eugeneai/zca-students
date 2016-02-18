.PHONY: init-python init-zca init test all

PY_DIR=python3
PYTHON=$(PY_DIR)/bin/python3
EI=$(PY_DIR)/bin/easy_install

all:	test

init-python:
	virtualenv3 $(PY_DIR)

init-zca: init-python
	$(EI) "zope.component [zcml]"

init:	init-zca

test:
	$(PYTHON) components.py
