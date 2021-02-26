FROM python:3.7-slim

WORKDIR /app

RUN pip install -U pandas google-cloud-storage sklearn

COPY test.py ./test.py

ENTRYPOINT [ "python3", "test.py" ]