import logging
import os
import sys

import argparse
import paramiko

from ..auxlib._is_slurm_job import is_slurm_job


def forward_to_slurm(args: argparse.Namespace) -> None:

    logging.info("Forwarding to SLURM via knockem cli...")

    env_dict = {
        k.replace("KNOCKEM_FWD__", ""): v
        for k, v in os.environ.items()
        if k.startswith("KNOCKEM")
    }
    env_words = [
        elem
        for key, value in env_dict.items()
        for elem in ["--env", f"{key}={value}"]
    ]
    invocation_words = [
        "singularity",
        *env_words,
        "run",
        f"docker://{os.environ['KNOCKEM_CONTAINER_IMAGE']}",
        *args.command,
    ]
    invocation = " ".join(invocation_words)
    logging.info(f"Invocation will be {invocation}")

    slurm_script = sys.stdin.read().replace(
        "{{{knockem_run_command}}}", invocation
    )

    # SSH connection parameters
    ssh_username = os.environ["KNOCKEM_SLURM_SSH_USERNAME"]
    ssh_hostname = os.environ["KNOCKEM_SLURM_SSH_HOSTNAME"]
    ssh_password = os.environ["KNOCKEM_SLURM_SSH_PASSWORD"]

    # Initialize SSH client
    logging.info("Initializing SSH client")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the server
    for attempt in range(5):
        logging.info(f"SLURM forward {attempt=}")
        try:
            ssh.connect(
                hostname=ssh_hostname,
                username=ssh_username,
                password=ssh_password,
                allow_agent=False,
                look_for_keys=False,
            )
            logging.info(f"SSH connection established to {ssh_hostname}")

            # Open an SFTP session
            sftp = ssh.open_sftp()

            # Create a temporary file for the SLURM script
            with sftp.file("slurm_job.sh", "w") as remote_file:
                remote_file.write(slurm_script)
            logging.info("SLURM script uploaded successfully.")

            # Ensure the script is executable
            ssh.exec_command("chmod +x slurm_job.sh")

            # Submit the SLURM job
            stdin, stdout, stderr = ssh.exec_command("sbatch slurm_job.sh")
            logging.info(f"SLURM job submitted.")
            logging.info(f"stdout:\n{stdout.read().decode('utf-8')}")
            logging.info(f"stderr:\n{stderr.read().decode('utf-8')}")

        except Exception as e:
            logging.error(f"SSH connection failed: {e}")

        finally:
            # Close the SSH client
            if ssh:
                ssh.close()
                logging.info("SSH connection closed.")
            return
