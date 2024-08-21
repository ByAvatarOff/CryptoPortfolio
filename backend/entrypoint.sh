alembic revision --autogenerate -m "init"
alembic upgrade head
cd src
uvicorn main:app --reload
