FROM python:3.9.5

# to make a persistent db on the same host machine
VOLUME /permutations_db

WORKDIR /permutations_app
COPY . /permutations_app

RUN pip install --no-cache-dir --upgrade -r /permutations_app/requirements.txt

RUN echo "Starting Preprocessing: mapping all words in db"
RUN python3 /permutations_app/utils/preprocess_main.py
RUN echo "Preprocessing is Done"

EXPOSE 8000

CMD ["uvicorn", "api.api_schema:api_handler", "--host", "0.0.0.0", "--port", "8000"]
