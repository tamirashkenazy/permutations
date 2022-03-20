FROM python:3.9.5

# to make a persistent db on the same host machine
VOLUME /permutations_db


WORKDIR /permutations_app

COPY ./requirements.txt /permutations_app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /permutations_app/requirements.txt

COPY ./api /permutations_app/api
COPY ./logger /permutations_app/logger
COPY ./paths /permutations_app/paths
COPY ./utils /permutations_app/utils
COPY ./db /permutations_app/db
COPY ./words_clean.txt /permutations_app/words_clean.txt

CMD ["python", "permutations_app/utils/preprocess_main.py"]

EXPOSE 8000

CMD ["uvicorn", "api.api_schema:api_handler", "--host", "127.0.0.1", "--port", "8000"]
