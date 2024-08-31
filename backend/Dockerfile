FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN pip install "poetry==1.7.1"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-root

COPY . .

ENTRYPOINT ["sh", "/backend/entrypoint.sh"]