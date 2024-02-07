import multiprocessing
import time

from connexion import AsyncApp
import schedule

from .service import handlers


def run_scheduler():
    schedule.every(20).seconds.do(handlers.run_handlers)
    while True:
        # schedule.run_pending()
        time.sleep(1)


app = AsyncApp(__name__)

# Add the API definition
app.add_api(f"{__file__}.openapi.yaml")

# Start scheduler in a separate process
scheduler_process = multiprocessing.Process(target=run_scheduler)
scheduler_process.start()

# Ensure the scheduler process is terminated when the main process exits
# scheduler_process.join()
