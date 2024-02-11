import os


def get_daemon_email() -> str:
    return os.environ.get("KNOCKEM_DAEMON_EMAIL", "mail@knockem.online")
