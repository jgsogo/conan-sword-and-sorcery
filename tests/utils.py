# -*- coding: utf-8 -*-

import contextlib
import os


@contextlib.contextmanager
def context_env(**environ):
    old_environ = dict(os.environ)
    os.environ.update(environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)