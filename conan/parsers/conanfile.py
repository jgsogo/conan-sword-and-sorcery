# -*- coding: utf-8 -*-

import sys
import logging

from conans.model.conan_file import ConanFile

log = logging.getLogger(__name__)


class ConanfileParser(object):
    """
    Parser for conanfile.py format
    """

    @staticmethod
    def parse(filename):
        log.debug("ConanfileParser::parse(filename='{0}') using python version '{1}'".format(filename, sys.version_info))
        # Follow https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
        if sys.version_info[0] < 3:
            import imp
            recipe = imp.load_source('r', filename)
            print(recipe)
        else:
            try:
                # Python 3.5+
                import inspect
                import importlib.util

                spec = importlib.util.spec_from_file_location("items", filename)
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)
                for name, obj in inspect.getmembers(foo, inspect.isclass):
                    if issubclass(obj, ConanFile) and name != ConanFile.__name__:
                        return obj

            except ImportError:
                # Python 3.3, 3.4
                from importlib.machinery import SourceFileLoader
                foo = SourceFileLoader("module.name", filename).load_module()
                print(foo)
