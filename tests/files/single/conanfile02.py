#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile


class Conanfile02(ConanFile):
    name = "protobuf"
    version = "3.5.1"
    settings = "os", "arch"
    options = {"shared": [True, False], }

