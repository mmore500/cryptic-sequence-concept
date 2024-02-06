import datetime
import functools
import os
import subprocess
import typing
import uuid
import warnings


def get_runmode() -> str:
    if "KNOCKEM_RUNMODE" not in os.env:
        warnings.warn("KNOCKEM_RUNMODE is unset, defaulting to 'testing'.")
    valid_runmodes = ("production", "testing")
    runmode = os.env("KNOCKEM_RUNMODE", "testing")
    if runmode not in valid_runmodes:
        raise ValueError(
            "environment variable KNOCKEM_RUNMODE must be one of "
            f"{valid_runmodes}, but was '{runmode}'.",
        )


@functools.lru_cache
def get_revision() -> str:
    return (
        subprocess.check_output(["git", "rev-parse", "HEAD", "--short"])
        .decode("ascii")
        .strip()
    )


def get_version() -> str:
    return "0.0.0"


def with_common_columns(*args: typing.List[str], **kwargs: dict) -> dict:
    res = {
        "datetime": str(datetime.datetime.now()),
        "knockemRunmode": get_runmode,
        "knockemRevision": get_revision(),
        "knockemVersion": get_version(),
        **kwargs,
    }
    id_ = str(uuid.uuid4())
    for idKey in args:
        res[idKey] = id_
    return res
