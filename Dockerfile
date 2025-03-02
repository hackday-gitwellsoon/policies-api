FROM python:3.11-slim

RUN apt-get update && \
    apt-get -y install libpango-1.0-0 libpangoft2-1.0-0

RUN pip install pymysql

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "main.py"]