# Установка зависимостей

`python -m venv venv`
`pip install -r requirements.txt`


# Окружения

## Окружение docker-compose

**Требование:** наличие переменных окружения `etc/.env.docker` и `infra/docker/local/.env` (примеры лежат рядом). 

**Запуск:**  `docker-compose -f infra/docker/local/docker-compose.yml up --build backend`

**Порты:** `app: 8001`, `pg: 5435`, `pg_test: 5436`  

## Локальное окружение

**Требование:** наличие переменных окружения `etc/.env.local` и `infra/docker/local/.env`

**Запуск БД и миграций:**  `docker-compose -f infra/docker/local/docker-compose.yml up --build migrations`

**Запуск:**  `uvicorn wallet.app:app --reload` или `make run`

## Окружение для запуска тестов 

**Требование:** наличие переменных окружения `etc/.env.tests_local`

**Запуск БД и миграций:**  `docker-compose -f infra/docker/local/docker-compose.yml up --build migrations_test`

**Запуск тестов:**  `pytest tests -vv` или `make tests`

# Линтеры

`ruff format .` или `make format`

`ruff check . --fix` или `make lint`

`mypy .` или `make mypy`,

или все сразу:

`make all`


# Ветки

```
main <- develop <- feature_branch
```

Пушить в develop и main нельзя 

Flow:

1) git switch develop
2) git update
3) git checkout -b feature/xxx
4) git add && git commit (message template: "#issue-number: comment")
5) Make PR
6) Approve PR
7) Merge branch to develop

