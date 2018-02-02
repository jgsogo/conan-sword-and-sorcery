#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile


class AllSettingsAndOptions(ConanFile):
    name = "settings_all_and_options"
    version = "1.8.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], }

