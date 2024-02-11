from ._get_url_base_path import get_url_base_path
from ._get_url_host import get_url_host


def get_url_submission_get(
    submissionId: str, apiKey: str = "{your api token here}"
) -> str:
    return (
        f"{get_url_host()}"
        f"{get_url_base_path()}"
        f"/submissions/{submissionId}?X-API-KEY={apiKey}"
    )
