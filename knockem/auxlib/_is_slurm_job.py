import os


def is_slurm_job():
    return "SLURM_JOB_ID" in os.environ
