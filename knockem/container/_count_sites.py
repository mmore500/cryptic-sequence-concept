import logging
import subprocess

from ..service import orchestration as orch


def count_sites(
    genomeContent: str,
    containerEnv: str,
    containerImage: str,
) -> int:
    command = [
        "singularity",
        "run",
        *containerEnv.split(),
        f"docker://{containerImage}",
        "knockem_count_sites",
    ]
    logging.info(f"Running count_sites with command: {' '.join(command)}")

    out, err = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    ).communicate(input=genomeContent.encode())
    try:
        return int(out)
    except ValueError as e:
        logging.error(f"count_sites failed with result {out}: {err}")
        raise e
