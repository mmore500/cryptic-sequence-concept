import time

import schedule

from . import handlers

if __name__ == "__main__":
    schedule.every(20).seconds.do(handlers.run_handlers)

    while True:
        schedule.run_pending()
        time.sleep(1)
