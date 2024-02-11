import os
import typing


def get_sendgrid_api_key() -> typing.Optional[str]:
    return os.environ.get("SENDGRID_API_KEY", None)
