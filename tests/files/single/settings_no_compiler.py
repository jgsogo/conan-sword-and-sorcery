#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile


class SettingsNoCompiler(ConanFile):
    name = "settings_no_compiler"
    version = "1.8.0"
    settings = "os", "arch", "build_type"
    options = {"option1": [True, False], }
