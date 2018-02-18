# -*- coding: utf-8 -*-

import os
import re
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


def parse_profile(profile_file):
    eq = re.compile("^([\w\.]+)=([\w_\+\.\s]+)\s")
    with open(profile_file) as f:
        matches = {}
        for line in f.readlines():
            m = eq.match(line)
            if m:
                matches[m.group(1)] = m.group(2)
    return matches
