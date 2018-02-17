# -*- coding: utf-8 -*-

import os
import tempfile
from contextlib import contextmanager


@contextmanager
def profile_for(compiler):
    # Create profile file
    tmp = tempfile.NamedTemporaryFile(dir=os.path.expanduser("~"), mode='w', delete=False)  # In local dirname
    tmp.write("include(default)\n\n")  # Profile 'default'
    tmp.write("[settings]\n")
    compiler.populate_profile_settings(tmp)
    tmp.write("[options]\n[build_requires]\n[env]\n")  # TODO: Is it needed?
    tmp.close()
    yield tmp.name
    os.unlink(tmp.name)

