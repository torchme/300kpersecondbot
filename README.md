1. pip install poetry
2. poetry install
3. pre-commit install

docker-compose -f docker/docker-compose.yml --env-file .env build

docker-compose -f docker/docker-compose.yml --env-file .env up
