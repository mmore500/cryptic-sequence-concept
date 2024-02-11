import os


def get_url_host() -> str:
    return os.environ.get("KNOCKEM_URL_HOST", "knockem.online")
