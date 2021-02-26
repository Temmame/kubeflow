FROM python:3.7-slim

WORKDIR /app

RUN pip install -U pandas google-cloud-storage 

COPY preprocess.py ./preprocess.py

ENTRYPOINT [ "python3", "preprocess.py" ]