import os
import typing


class Services(typing.NamedTuple):
    MICHELANGELO_SERVICE_URL = os.getenv("MICHELANGELO_SERVICE_URL")
    DONATELLO_SERVICE_URL = os.getenv("DONATELLO_SERVICE_URL")
