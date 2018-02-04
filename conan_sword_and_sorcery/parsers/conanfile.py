# -*- coding: utf-8 -*-

import sys
import logging
import inspect
import itertools


from conans.model.conan_file import ConanFile

log = logging.getLogger(__name__)


class ConanfileWrapper(object):
    """
    Parser for conanfile.py recipes
    """

    def __init__(self, recipe_class):
        assert(issubclass(recipe_class, ConanFile))
        self.recipe_class = recipe_class

    @staticmethod
    def parse(filename):
        log.debug("ConanfileParser::parse(filename='{0}') using python version '{1}'".format(filename, sys.version_info))
        # Follow https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
        if sys.version_info[0] < 3:
            import imp
            foo = imp.load_source(filename, filename)  # First parameter uses filename so each .py is loaded in a module with a different name
        else:
            try:
                # Python 3.5+
                import importlib.util
                spec = importlib.util.spec_from_file_location("items", filename)
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)

            except AttributeError:
                # Python 3.3, 3.4
                from importlib.machinery import SourceFileLoader
                foo = SourceFileLoader("module.name", filename).load_module()

        for name, obj in inspect.getmembers(foo, inspect.isclass):
            if issubclass(obj, ConanFile) and name != ConanFile.__name__:
                return ConanfileWrapper(obj)

        raise ValueError("Cannot load conan_sword_and_sorcery recipe from filename '{}'".format(filename))

    def __getattr__(self, item):
        return getattr(self.recipe_class, item)

    def conjugate_options(self, options):
        to_conjugate = []
        for opt in options:
            idx = list(self.options.keys()).index(opt)
            to_conjugate.append(list(self.options.values())[idx])
        if len(to_conjugate):
            return itertools.product(*to_conjugate)
        return None

