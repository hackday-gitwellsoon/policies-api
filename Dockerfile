FROM python:3.11-slim

RUN pip install pymysql

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "main.py"]