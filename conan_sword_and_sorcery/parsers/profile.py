# -*- coding: utf-8 -*-

import os
import tempfile
from contextlib import contextmanager
import configparser


@contextmanager
def profile_for(compiler, basepath=None):
    # Create profile file
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform=str
    config["settings"] = {}
    config["env"] = {}
    config["build_requires"] = {}
    compiler.populate_profile(config)

    # Dump it to a system file
    basepath = basepath or os.path.expanduser("~")
    tmp = tempfile.NamedTemporaryFile(dir=basepath, mode='w', delete=False)  # In local dirname
    config.write(tmp)
    tmp.close()

    yield tmp.name

    os.unlink(tmp.name)


def parse_profile(profile_file):
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.optionxform = str
    parser.read(profile_file)
    return parser
