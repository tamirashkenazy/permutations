FROM python:3.9.5

EXPOSE 8000

WORKDIR /pa-permutations

COPY ./requirements.txt /pa-permutations/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /pa-permutations/requirements.txt

COPY ./api /pa-permutations/api
COPY ./logger /pa-permutations/logger
COPY ./paths /pa-permutations/paths
COPY ./utils /pa-permutations/utils

CMD ["uvicorn", "api.api_schema:api_handler", "--host", "127.0.0.1", "--port", "8000"]
