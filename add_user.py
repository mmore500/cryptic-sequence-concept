#!/usr/bin/env python3.10

import sys

from knockem.service.orchestration import add_user, has_user

if __name__ == "__main__":

    __, user = sys.argv

    print(add_user(user))
    assert has_user
