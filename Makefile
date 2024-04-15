SHELL := /bin/bash

install:
	pip install poetry
	poetry install

auth:
	echo $(PREFECT_API_KEY)
	poetry run prefect cloud login --key $(PREFECT_API_KEY) --workspace $(PREFECT_WORKSPACE_ID)

run:
	poetry run sh commands/prefect.sh
