# -*- coding: utf-8 -*-

import os
import tempfile
from contextlib import contextmanager


@contextmanager
def profile_for(compiler):
    # Create profile file
    fd, path = tempfile.mkstemp()
    with open(fd, 'w') as tmp:
        tmp.write("include(default)\n\n")  # Profile 'default'
        tmp.write("[settings]\n")
        compiler.populate_profile_settings(tmp)
        tmp.write("[options]\n[build_requires]\n[env]\n")  # TODO: Is it needed?
    # os.close(fd)
    yield path

    os.remove(path)

