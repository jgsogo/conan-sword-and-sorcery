# -*- coding: utf-8 -*-

import itertools
from operator import itemgetter

from .settings import get_settings
from conan.parsers.conanfile import ConanfileWrapper
from conans.model.settings import Settings


class Executor(object):

    def __init__(self, conanfile, os_system=None):
        self._all_settings = list(get_settings(os_system))
        self._conanfile_wrapper = ConanfileWrapper.parse(conanfile)

        # Group settings by compiler
        for compiler, group in itertools.groupby(self._all_settings, itemgetter(1)):
            for os_system, compiler, items in group:
                print(items)
                settings = Settings({'os': [items['os'], ],
                                     'arch': items['archs'],
                                     'build_type': items['build_types'],
                                     'compiler.version': items['versions'],
                                     'compiler.name': compiler.compiler,
                                     'compiler': compiler.compiler,
                                     })

                from pprint import pprint
                pprint(settings._data)

                recipe = self._conanfile_wrapper.recipe_class(output=None, runner=None, settings=settings)
                recipe.configure()
