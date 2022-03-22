import logging
import sys
import time
import os.path as path
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.background import BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
from fastapi_utils.timing import add_timing_middleware

from similar_words.preprocess import populate_similar_words

BASE_APP_DIR_PATH = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_APP_DIR_PATH)

from logger.api_logger import get_stream_handler
from api.definitions import PermutationResponse


api_handler = FastAPI(
    title="Permutations Api Schema", docs_url=None, redoc_url=None, openapi_url=""
)

# region Logging
api_logger = logging.getLogger(__name__)
api_logger.setLevel(logging.DEBUG)

api_logger.addHandler(get_stream_handler(sys.stdout, logging.DEBUG))
api_logger.addHandler(get_stream_handler(sys.stderr, logging.ERROR))
# endregion

all_words_map = populate_similar_words()

add_timing_middleware(
    api_handler, record=api_logger.info, prefix="api", exclude="get_statistics"
)

api_handler.add_middleware(
    CORSMiddleware,
    # TODO - remove the star and specify origins
    allow_origins=["http://localhost:8000"],
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
    return "Health Check OK\n"


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
    start = time.process_time_ns()
    list_of_permutations = all_words_map.get_list_of_permutations(word)
    end = time.process_time_ns()
    total_time_in_ns = end - start
    # this task will execute after the response
    background_tasks.add_task(all_words_map.update_avg_and_reqs_stats, total_time_in_ns)
    return {"similar": list_of_permutations}


@api_handler.get("/api/v1/stats", status_code=status.HTTP_200_OK)
def get_statistics():
    return all_words_map.stats


if __name__ == "__main__":
    uvicorn.run("api_schema:api_handler", host="0.0.0.0", port=8000, reload=True)
