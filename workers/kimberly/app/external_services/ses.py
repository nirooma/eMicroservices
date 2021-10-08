from typing import List

import boto3
import logging
from core.config import region_name

from core.config import aws_access_key_id, aws_secret_access_key

logger = logging.getLogger(__name__)


def _get_client():
    """ Return AWS client """
    return boto3.client(
        'ses',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )


def send_mail(recipients: List[str], subject: str, data: str = "TEST"):
    charset = "UTF-8"
    try:
        response = _get_client().send_email(
            Destination={
                "ToAddresses": recipients,
            },
            Message={
                "Body": {
                    "Text": {
                        "Charset": charset,
                        "Data": data,
                    }
                },
                "Subject": {
                    "Charset": charset,
                    "Data": subject,
                },
            },
            Source="nirooma@icloud.com",
        )
        logger.info(f"Email sent to {recipients=} with status code {response['ResponseMetadata']['HTTPStatusCode']}")
        return response

    except Exception as e:
        logger.exception(f"Couldn't send email to {recipients=}", exc_info=e)
        return False


