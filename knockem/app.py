import logging
import multiprocessing
import signal
import sys
import time

from connexion import AsyncApp
from connexion.exceptions import OAuthProblem
import schedule

from .service import handlers, orchestration

_interrupted = 0


def _interrupt(signal, frame) -> None:
    global _interrupted
    _interrupted += 1
    if _interrupted == 1:
        logging.info(
            "Interrupted! Completing current tasks and shutting down. "
            "Interrupt again to force shutdown.",
        )
    else:
        logging.info(
            f"Interrupted count {_interrupted}. Forcefully shutting down.",
        )
        sys.exit(1)


signal.signal(signal.SIGINT, _interrupt)


def run_scheduler():
    schedule.every(10).seconds.do(handlers.run_handlers)
    while not _interrupted:
        logging.info("Scheduler loop.")
        schedule.run_pending()
        time.sleep(1)

    logging.info("Work completed. Shutting down.")
    sys.exit(0)


def apikey_auth(token, required_scopes) -> dict:
    if not orchestration.has_api_token(token):
        raise OAuthProblem("Invalid token")

    return {}


logging.basicConfig(level=logging.INFO)

app = AsyncApp(__name__)

# Add the API definition
app.add_api(f"{__file__}.openapi.yaml")

# Start scheduler in a separate process
scheduler_process = multiprocessing.Process(target=run_scheduler)
scheduler_process.start()

# Ensure the scheduler process is terminated when the main process exits
# scheduler_process.join()
