import logging
import subprocess


def compete_two(containerImage: str, envArgs: str) -> None:
    command = [
        "singularity",
        "run",
        # "--env",  # this should already be in env and get passed thru
        # 'KNOCKEM_RECORDS_URI="${KNOCKEM_RECORDS_URI}"',
        *envArgs.split(),
        f"docker://{containerImage}",
        "knockem_compete_two",
    ]
    logging.info(f"Running competition with command: {' '.join(command)}")
    subprocess.Popen(command)
