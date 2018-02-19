# -*- coding: utf-8 -*-

import os
import logging

log = logging.getLogger(__name__)


def cmd(command, exception=RuntimeError, secret=False):
    r = os.system(command)
    if r != 0:
        raise exception("Error running command '{}'".format(command if not secret else '**secret**'))
    return r
