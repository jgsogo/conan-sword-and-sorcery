#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile


class Conanfile01(ConanFile):
    name = "gtest"
    version = "1.8.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "build_gmock": [True, False], "fpic": [True, False]}
    default_options = ("shared=True", "build_gmock=False", "fpic=True")

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fpic")

