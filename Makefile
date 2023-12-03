lint: FORCE
	ruff check . --fix

format: FORCE
	ruff format .

mypy: FORCE
	mypy .

all: lint format mypy

migrate: FORCE
	migrate -path ./infra/postgres/migrations -database "postgres://wallet:wallet@localhost:5436/wallet?sslmode=disable" up

migrate_test: FORCE
	migrate -path ./infra/postgres/migrations -database "postgres://wallet:wallet@localhost:5435/wallet_test?sslmode=disable" up

tests: FORCE
	pytest tests -vv

run:
	uvicorn wallet.app:app --reload --log-level info

FORCE: ;
