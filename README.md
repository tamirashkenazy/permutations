how to build docker image: 

cd Dockerfile/path

docker build -t permutations-image .

how to run:

docker run -d --name permutations-container -p 8000:8000 permutations-image


check that api is running:

curl "http://127.0.0.1:8000/health"

should get:

Health Check OK


get word example:

curl "http://localhost:8000/api/v1/similar?word=apple"

should get:

{"similar":["appel","pepla"]}