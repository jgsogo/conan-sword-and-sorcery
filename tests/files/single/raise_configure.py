#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile
from conans.errors import ConanException


class RaiseConfigureWindowsSettings(ConanFile):
    name = "settings_all"
    version = "1.8.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {'opt1': [True, False]}
    default_options = "opt1=True"

    def configure(self):
        if self.settings.os == 'Windows':
            raise ConanException("Windows operating system is not supported")

        if self.settings.os == 'Linux':
            if not self.options.opt1:
                raise ConanException("Linux with option opt1=False is not supported")
