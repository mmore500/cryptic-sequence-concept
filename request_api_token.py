#!/usr/bin/env python3.10

import sys

from knockem.service.orchestration import add_api_token

if __name__ == "__main__":

    __, user = sys.argv

    print(add_api_token(user))
