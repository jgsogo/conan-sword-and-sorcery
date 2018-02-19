# -*- coding: utf-8 -*-

import uuid
import logging
from contextlib import contextmanager
from conan_sword_and_sorcery.utils.cmd import cmd

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
