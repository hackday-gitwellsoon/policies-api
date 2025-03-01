FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt /app

COPY . /app

CMD ["python", "main.py"]