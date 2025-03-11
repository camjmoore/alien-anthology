FROM python:3.10.12

WORKDIR /alien-anthology-api

COPY api/requirements.txt ./api-requirements.txt
COPY shared/database/requirements.txt ./database-requirements.txt

RUN pip install --no-cache-dir -r ./api-requirements.txt -r ./database-requirements.txt

COPY api/ ./api/
COPY shared/ ./shared/
COPY config.yaml ./config.yaml

CMD ["fastapi", "run", "api/main.py", "--port", "80"]
