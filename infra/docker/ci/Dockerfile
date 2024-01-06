FROM python:3.12 as base-app

WORKDIR /app
COPY requirements.txt pyproject.toml ./
RUN pip install -r requirements.txt

FROM base-app as backend
# Copy Application
COPY ./wallet /app/wallet
COPY ./etc/.env.docker /app/etc/.env
ENV CONFIG_NAME=".env"
ENV PYTHONPATH="/"

CMD uvicorn wallet.app:app --host 0.0.0.0 --port 8080