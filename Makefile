build:
	docker compose -f docker-compose.yml build

up:
	docker compose -f docker-compose.yml up -d

stop:
	docker compose -f docker-compose.yml stop

restart:
	docker compose -f docker-compose.yml stop && docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down -v

logs:
	docker compose -f docker-compose.yml logs -f web