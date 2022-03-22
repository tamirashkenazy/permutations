FROM python:3.9.5

WORKDIR /permutations_app
COPY . /permutations_app

RUN pip install --no-cache-dir --upgrade -r /permutations_app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api.api_schema:api_handler", "--host", "0.0.0.0", "--port", "8000"]
