.PHONY: up down build logs test seed

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

test:
	docker-compose run --rm backend pytest

seed:
	docker-compose run --rm backend python scripts/seed_database.py
