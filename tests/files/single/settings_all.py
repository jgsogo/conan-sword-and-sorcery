#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile


class JustAllSettings(ConanFile):
    name = "settings_all"
    version = "1.8.0"
    settings = "os", "arch", "compiler", "build_type"

