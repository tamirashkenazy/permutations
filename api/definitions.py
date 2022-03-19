from typing import List

from pydantic import BaseModel


class PermutationResponse(BaseModel):
    similar: List[str]


class StatisticsResponse(BaseModel):
    totalWords: int
    totalRequests: int
    avgProcessingTimeNs: int
