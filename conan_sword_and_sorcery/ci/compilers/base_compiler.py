# -*- coding: utf-8 -*-

import os
import subprocess
import logging
from conan_sword_and_sorcery.utils import isstr

log = logging.getLogger(__name__)


class BaseCompiler(object):
    id = None
    osys = None

    def __init__(self, **kwargs):
        self._data = kwargs

        # Validate input arguments
        for key, val in kwargs.items():
            if not val or not isstr(val):
                raise ValueError("Invalid configuration argument for compiler '{}': argument '{}' must be a non empty string.".format(self.id, key))

    def __getattr__(self, item):
        if item == 'os':
            return self.osys
        return self._data.get(item)

    def update_settings(self, settings):
        settings.build_type = self.build_type
        settings.arch = self.arch
        settings.compiler = self.id
        settings.compiler.version = self.version

    def populate_profile_settings(self, f):
        f.write("arch={}\n".format(self.arch))
        f.write("build_type={}\n".format(self.build_type))
        f.write("compiler={}\n".format(self.id))
        f.write("compiler.version={}\n".format(self.version))

    @classmethod
    def validate(cls, **kwargs):
        # Raise error if given configuration is not supported
        return True

    @classmethod
    def environment_filters(cls):
        raise NotImplementedError

    def run(self, command_plain, dry_run=False):
        log.debug("BaseCompiler::run")
        log.info("command to run: {}".format(command_plain))
        if not dry_run:
            ret = os.system(command_plain)  # TODO: May use subprocess
            return "OK" if ret == 0 else "FAIL"
        return "DRY_RUN"

