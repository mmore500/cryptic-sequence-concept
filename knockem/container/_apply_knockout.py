import logging
import subprocess


def apply_knockout(
    genomeContent: str,
    knockoutSites: str,
    containerEnv: str,
    containerImage: str,
) -> str:
    command = [
        "singularity",
        "run",
        *containerEnv.split(),
        f"docker://{containerImage}",
        "knockem_apply_knockout",
        *knockoutSites.split(),
    ]
    logging.info(f"Running count_sites with command: {' '.join(command)}")

    out, err = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    ).communicate(input=genomeContent.encode())
    return out
