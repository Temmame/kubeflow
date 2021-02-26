FROM python:3.7-slim

WORKDIR /app

RUN pip install -U pandas sklearn google-cloud-storage

COPY train.py ./train.py

ENTRYPOINT [ "python3", "train.py" ]