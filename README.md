# Permutations App 

by Tamir Ashkenazy

## Installation

### Build docker image:
#### pre-build - Remove Volume:
* `docker volume rm permutations_db`

_building the docker is executing pre-processing section_
* `cd /path/to/pa-permutation`
* `docker build -t permutations-image .`


### Run docker image:
#### First docker with volume definition
* `docker run -d --name=permutations-container -p 8000:8000 -v permutations_db:/permutations_db permutations-image`

#### Dockers with the first docker volume attached
* `docker run -d --name=permutations-container-2 -p 8001:8000 --volumes-from permutations-container permutations-image`

## Documentation

### Check Health of WebService:
* `curl "http://127.0.0.1:8000/health"`

Expected Response: 
```
Health Check OK
```


### GET request for similar words:
* `curl "http://localhost:8000/api/v1/similar?word=<some_word>"`

Response:
```
{
    similar: [list,of,words,that,are,similar,to,provided,word]
}
```

### GET request for statistics:
* `curl "http://localhost:8000/api/v1/stats"`


Response:
```
{
    totalWords: int
    totalRequests: int
    avgProcessingTimeNs: int
}
```


