import base64
import json
from typing import Dict, Any

from fastapi import status

from app.core.configuration_utils import config


def _response(
        detail=config.get("defaultAnswer"),
        status_code=status.HTTP_200_OK,
        **kwargs
):
    return {"detail": detail, "status": status_code, **kwargs}


def encode_base64(data: Dict[str, Any]) -> str:
    """ Receive a dict and return a encode base64 string """
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()


def decode_base64(string_: str) -> Dict:
    """ Receive a string and return encode from base64 dict """
    return json.loads(base64.urlsafe_b64decode(string_).decode())
