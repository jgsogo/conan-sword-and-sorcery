# -*- coding: utf-8 -*-

import sys
import logging
import inspect
import itertools
from copy import deepcopy

from conans.model.conan_file import ConanFile
from conans.model.settings import Settings

log = logging.getLogger(__name__)


class ConanFileWrapper(object):
    """ Parser for conanfile.py recipes """

    def __init__(self, recipe_class):
        assert issubclass(recipe_class, ConanFile)
        self.recipe_class = recipe_class
        self.recipe = None

    def __str__(self):
        return "{}/{}".format(self.recipe_class.name, self.recipe_class.version)

    @staticmethod
    def parse(filename):
        log.debug("ConanfileParser::parse(filename='{0}')".format(filename))
        log.debug(" - using python version '{}".format(sys.version_info))
        # Follow https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
        if sys.version_info[0] < 3:  # pragma: no py3 cover
            import imp
            try:
                foo = imp.load_source(filename, filename)  # First parameter uses filename so each .py is loaded in a module with a different name
            except IOError:
                raise IOError("Cannot import filename '{}'".format(filename))
        else:  # pragma: no py2 cover
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
                return ConanFileWrapper(obj)

        raise ValueError("Cannot load conan_sword_and_sorcery recipe from filename '{}'".format(filename))

    def instantiate(self, settings):  # type: (Settings) -> None
        self.recipe = self.recipe_class(output=None, runner=None, settings=settings)

    def reset_recipe(self, settings):  # type: (Settings) -> None
        self.instantiate(settings=settings)
        # TODO: This is almost a Conan issue: a need to make this method available because I cannot reset options,
        #   I cannot do a `self.recipe.options = conans.model.conan_file.create_options(self.recipe)` because the
        #   the value self.recipe.options (which is used inside create_options is no longer a dictionary.

    def settings_keys(self):
        if not self.recipe:
            raise RuntimeError("Instantiate recipe first")
        return self.recipe.settings._data.keys()

    def options_keys(self):
        if not self.recipe:
            raise RuntimeError("Instantiate recipe first")
        return self.recipe.options._data.keys()

    def options_values(self, option_key):
        return self.recipe_class.options[option_key]

    def __getattr__(self, item):
        if not self.recipe:
            raise RuntimeError("Instantiate recipe first")
        return getattr(self.recipe, item)

    def conjugate_options(self, options):
        to_conjugate = []
        for opt in options:
            to_conjugate.append(self.options_values(opt))
        if len(to_conjugate):
            return itertools.product(*to_conjugate)
        return None

