import os


def get_admin_email() -> str:
    return os.environ.get("KNOCKEM_ADMIN_EMAIL", "morenoma@umich.edu")
