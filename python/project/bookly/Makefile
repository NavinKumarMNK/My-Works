DEV_ENV_NAME = 'bookly_dev'
DOCKER_COMPOSE_FILE_NAME = 'docker-compose.yaml'

up:
	docker-compose -p $(DEV_ENV_NAME) -f $(DOCKER_COMPOSE_FILE_NAME) up

logs:
	docker-compose -p $(DEV_ENV_NAME) logs -f

attach:
	docker-compose -p $(DEV_ENV_NAME) exec web bash

attach-postgres:
	docker-compose -p $(DEV_ENV_NAME) exec postgres bash


build:
	docker-compose -p $(DEV_ENV_NAME) -f $(DOCKER_COMPOSE_FILE_NAME) build

run:
	make build
	make up