# -*- coding: utf-8 -*-

import os
import logging

log = logging.getLogger(__name__)


def cmd(command, exception=RuntimeError, error_msg="Error running command '{command}'", secret=False):
    log.debug("Run command: {}".format(command if not secret else '**secret**'))
    r = os.system(command)
    if r != 0:
        msg = error_msg.format(command=command if not secret else '**secret**')
        if exception:
            raise exception(msg)
        else:
            log.error(msg)
    return r
