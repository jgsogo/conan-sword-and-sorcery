# -*- coding: utf-8 -*-

import logging

from conan_sword_and_sorcery.utils import isstr

log = logging.getLogger(__name__)


class BaseCompiler(object):
    id = None
    osys = None
    _required_init_arguments = []

    def __init__(self, **kwargs):
        self._data = kwargs
        self.cmd = None  # Will be set by the runner

        # Validate input arguments
        for key, val in kwargs.items():
            if not val or not isstr(val):
                raise ValueError("Invalid configuration argument for compiler '{}': argument '{}' must be a non empty string.".format(self.id, key))
        # Check that all required arguments are set
        for required_arg in self._required_init_arguments:
            if required_arg not in kwargs.keys():
                raise ValueError("Required argument '{}' for compiler '{}' not set in initialization.".format(required_arg, self.id))

    def __getattr__(self, item):
        if item == 'os':
            return self.osys
        return self._data.get(item)

    def update_settings(self, settings):
        settings.build_type = self.build_type
        settings.arch = self.arch
        settings.compiler = self.id
        settings.compiler.version = self.version

    def populate_profile(self, configfile):
        configfile['settings']['os'] = self.osys
        configfile['settings']['arch'] = self.arch
        configfile['settings']['build_type'] = self.build_type
        configfile['settings']['compiler'] = self.id
        configfile['settings']['compiler.version'] = self.version

    @classmethod
    def validate(cls, **kwargs):
        # Raise error if given configuration is not supported
        return True

    @classmethod
    def environment_filters(cls):
        raise NotImplementedError("Compiler must explicitly declare its environment filters.")

    def run(self, command_plain):
        log.debug("BaseCompiler::run")
        return self.cmd(command_plain)

