import logging
from typing import TextIO

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def get_stream_handler(sys_io: TextIO, logging_level: int):
    stdout_stream_handler = logging.StreamHandler(sys_io)
    stdout_stream_handler.setLevel(level=logging_level)
    stdout_stream_handler.setFormatter(formatter)
    return stdout_stream_handler
