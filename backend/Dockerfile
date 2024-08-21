FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod g+x /backend/entrypoint.sh
ENTRYPOINT ["sh", "/backend/entrypoint.sh"]