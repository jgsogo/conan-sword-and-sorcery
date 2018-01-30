# -*- coding: utf-8 -*-

import os
import itertools
import logging
import platform
from collections import defaultdict

from conans.util.env_reader import get_env
from conan.utils import isstr
from conan.ci.compilers import Compiler
from conans.model.settings import Settings as ConanSettings

log = logging.getLogger(__name__)


class Settings:

    @classmethod
    def default(cls):
        filename = os.path.join(os.path.dirname(__file__), '..', 'conan_settings.yaml')
        with open(filename, 'r') as f:
            return ConanSettings.loads(f.read())

    def __init__(self, settings_filename=None):
        if settings_filename:
            with open(settings_filename, 'r') as f:
                self.conan_settings = ConanSettings.loads(f.read())
        else:
            self.conan_settings = Settings.default()

    def current(self, compiler, arch, build_type, version, **kwargs):
        self.conan_settings.os = compiler.os_system
        self.conan_settings.arch = arch
        self.conan_settings.build_type = build_type
        self.conan_settings.compiler = compiler.compiler
        self.conan_settings.compiler.version = version
        return self.conan_settings


