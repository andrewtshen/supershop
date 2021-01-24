# WORK IN PROGRESS: DON'T USE

DEBUG ?= 1
PROJECT = project

.PHONY: all
all: venv/
	. venv/bin/activate
	@flask run

.PHONY: install
install: refresh venv/
	@export FLASK_APP="$(PROJECT)"
	@export FLASK_DEBUG=$(DEBUG)

venv/: requirements.txt
	@pip3 install virtualenv
	@virtualenv venv
	. venv/bin/activate && pip install -r requirements.txt

.PHONY: refresh
refresh:
	@python refresh_dbs.py

.PHONY: clean
clean:
	. deactivate
	@rm -rf *.sqlite
