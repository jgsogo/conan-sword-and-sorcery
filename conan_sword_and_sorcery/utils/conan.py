# -*- coding: utf-8 -*-

import os
import uuid
import logging
from contextlib import contextmanager
from configparser import ConfigParser
from conan_sword_and_sorcery.utils.cmd import cmd
from conan_sword_and_sorcery.utils import backup_file

log = logging.getLogger(__name__)


@contextmanager
def remote(url, name=None, insert_first=True):
    name = name or uuid.uuid4()
    command = "conan remote add {name} {url}".format(name=name, url=url)
    if insert_first:
        command += " --insert 0"

    cmd(command)
    yield name
    cmd("conan remote remove {name}".format(name=name))


def remote_auth(remote, username, password):
    command = "conan user -p {password} -r {remote} {username}".format(username=username, remote=remote, password=password)
    cmd(command, secret=True)


@contextmanager
def conf(new_values, conan_conf=None):
    conan_conf = conan_conf or os.path.join(os.path.expanduser("~"), '.conan', 'conan.conf')
    if not os.path.exists(conan_conf):
        raise RuntimeError("Cannot find configuration file at '{}'".format(conan_conf))

    with backup_file(conan_conf):
        config = ConfigParser()
        config.optionxform = str
        config.read(conan_conf)
        for section, item, new_value in new_values:
            config[section][item] = new_value

        with open(conan_conf, 'wb') as output_config:
            config.write(output_config)
        yield config

    pass

