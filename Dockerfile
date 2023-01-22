FROM python:3.11-slim-bullseye

EXPOSE 8080

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV FACEIT_API_KEY=NA
ENV FACEIT_PLAYER_ID=NA
ENV NUMBERS_OF_MATCHES=NA
ENV BOT_TOKEN=NA
ENV BOT_CHANNEL_ID=NA

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /src
COPY src/ /src/

CMD uvicorn main:api --host 0.0.0.0 --port 8080
