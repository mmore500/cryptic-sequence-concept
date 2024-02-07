#!/usr/bin/env python3.10

import sys

from knockem.common.records import purge_testing as purge_records
from knockem.service.orchestration import purge_testing as purge_orchestration

if __name__ == "__main__":

    purge_records()
    purge_orchestration()
