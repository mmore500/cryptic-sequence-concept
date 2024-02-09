import logging
import multiprocessing
import time

from connexion import AsyncApp
import schedule

from .service import handlers


def run_scheduler():
    schedule.every(10).seconds.do(handlers.run_handlers)
    while True:
        logging.info("Scheduler loop.")
        schedule.run_pending()
        time.sleep(5)


logging.basicConfig(level=logging.INFO)

app = AsyncApp(__name__)

# Add the API definition
app.add_api(f"{__file__}.openapi.yaml")

# Start scheduler in a separate process
scheduler_process = multiprocessing.Process(target=run_scheduler)
scheduler_process.start()

# Ensure the scheduler process is terminated when the main process exits
# scheduler_process.join()
