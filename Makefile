SHELL := /bin/bash

run:
	export FLASK_APP=manage.py
	flask process_batch
