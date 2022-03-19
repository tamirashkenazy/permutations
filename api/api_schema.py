import logging
import sys
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.background import BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
from fastapi_utils.timing import add_timing_middleware
import os.path as path

absolute_project_path = path.dirname(path.abspath(__file__))
sys.path.append(absolute_project_path)

from logger.api_logger import get_stream_handler
from api.definitions import PermutationResponse
from utils.permutations_utils import (
    sort_a_word,
    get_list_of_permutations_from_a_file,
    add_statistics_of_requests,
)

api_handler = FastAPI(
    title="Permutation Api Schema", docs_url=None, redoc_url=None, openapi_url=""
)

# region Logging
api_logger = logging.getLogger(__name__)
api_logger.setLevel(logging.DEBUG)

api_logger.addHandler(get_stream_handler(sys.stdout, logging.INFO))
api_logger.addHandler(get_stream_handler(sys.stderr, logging.ERROR))
# endregion

add_timing_middleware(
    api_handler, record=api_logger.info, prefix="api", exclude="get_statistics"
)

api_handler.add_middleware(
    CORSMiddleware,
    # TODO - remove the star and specify origins
    allow_origins=["*"],
    allow_credentials=True,
    # allow_methods: any HTTP Request
    allow_methods=["*"],
    allow_headers=["*"],
)


@api_handler.get(
    "/health",
    response_model=str,
    status_code=status.HTTP_200_OK,
)
def get_health_message():
    return "Health Check OK"


# TODO - add exception handler for errors and exceptions
@api_handler.get(
    "/api/v1/similar",
    response_model=PermutationResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_permutations_of_word_from_file(
    background_tasks: BackgroundTasks, word: str = ""
):
    if word == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Got an empty word, please provide word=<some_word>",
        )
    sorted_word = sort_a_word(word)
    list_of_permutations = get_list_of_permutations_from_a_file(sorted_word)
    # this task will execute after the response
    measured_time_in_nano = 100
    background_tasks.add_task(add_statistics_of_requests, measured_time_in_nano)
    return {"similar": list_of_permutations}


@api_handler.get("/api/v1/stats", status_code=status.HTTP_200_OK)
def get_statistics():
    nano_seconds = 45000
    total_words = 100
    total_requests = 10

    return {
        "totalWords": total_words,
        "totalRequests": total_requests,
        "avgProcessingTimeNs": nano_seconds,
    }


if __name__ == "__main__":
    # instructions to setup PyCharm for controller debugging:
    # https://seg-confluence.csg.apple.com/display/CELLULAR/Debugging
    uvicorn.run("api_schema:api_handler", host="127.0.0.1", port=8000, reload=True)
