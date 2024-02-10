import logging

import subprocess


def warm_image_cache(containerImage: str) -> None:
    command = ["singularity", "run", f"docker://{containerImage}", "true"]
    logging.info(f"Warming cache with command: {' '.join(command)}")
    subprocess.Popen(command).wait()  # ensure cache ready before proceeding
