#!/usr/bin/env python

import os
import sys

from cryptography.fernet import Fernet


def generate_key(filename):
    key = Fernet.generate_key()

    with open(filename, 'wb') as f:
        f.write(key)

generate_key(sys.argv[1])

