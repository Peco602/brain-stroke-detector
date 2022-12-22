SHELL:=/bin/bash

prerequisites: ## Perform the initial machine configuration
	@sudo apt update
	@sudo apt install docker.io python3.9 python3-pip -y
	@sudo pip install pipenv
	@sudo wget https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-linux-x86_64 -O /usr/bin/docker-compose
	@sudo chmod +x /usr/bin/docker-compose

setup: ## Setup the development environment
	@pipenv install --dev; pipenv run pre-commit install

train: ## Train the model
	@pipenv run python train.py

test: ## Run the unit tests
	@pytest tests -v -s

quality-checks: ## Perform the code quality checks
	isort .
	black .
	pylint --recursive=y .

build: ## Build the stroke detector docker image
	@docker-compose build

publish: tests quality-checks build ## Publish the stroke detector docker image to DockerHub
	@docker login
	@docker-compose push

pull: ## Pull latest images
	@docker-compose pull

run: ## Run the stroke detector docker image
	@docker-compose up -d

logs: ## Check the stroke detector docker image
	@docker-compose logs -f

restart: ## Restart the stroke detector docker image
	@docker-compose restart

kill: ## Kill the stroke detector docker image
	@docker-compose down

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
