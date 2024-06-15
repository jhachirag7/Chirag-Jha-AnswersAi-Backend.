FROM python:3.12.3-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /fastapi_answerai
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
COPY . .