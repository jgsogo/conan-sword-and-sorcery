# -*- coding: utf-8 -*-

import os
import tempfile
from contextlib import contextmanager
import configparser


@contextmanager
def profile_for(compiler):
    # Create profile file
    config = configparser.ConfigParser()
    config.optionxform=str
    config["settings"] = {}
    config["env"] = {}
    compiler.populate_profile(config)

    # Dump it to a system file
    tmp = tempfile.NamedTemporaryFile(dir=os.path.expanduser("~"), mode='w', delete=False)  # In local dirname
    config.write(tmp)
    tmp.close()

    yield tmp.name

    os.unlink(tmp.name)


def parse_profile(profile_file):
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read(profile_file)
    return parser
