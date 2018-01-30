# -*- coding: utf-8 -*-

import itertools
import logging
from operator import itemgetter
from conans.errors import ConanException

from conan.parsers.conanfile import ConanfileWrapper
from conan.ci.settings import Settings
from conan.ci.compilers import get_available_configurations

log = logging.getLogger(__name__)


class Executor:
    def __init__(self, conanfile, os_system=None):
        log.debug("Executor::__init__(conanfile='{}', os_system='{}')".format(conanfile, os_system))
        self._settings = Settings()
        self._conanfile_wrapper = ConanfileWrapper.parse(conanfile)

    def enumerate_jobs(self):
        log.debug("Executor::enumerate_jobs")
        recipe = self._conanfile_wrapper.recipe_class(output=None, runner=None, settings=self._settings.conan_settings)

        settings_in_recipe = list(self._settings.conan_settings._data.keys())
        settings_in_recipe = settings_in_recipe + ['version', 'runtime',]

        # Get all compilers and configurations available for this operating system
        for compiler, configurations in get_available_configurations(allow_configurations=settings_in_recipe):
            for items in configurations:
                log.debug(" - set_current({}, {}, {})".format(compiler.os_system, compiler.compiler, items))
                self._settings.current(compiler=compiler, **items)
                try:
                    recipe.configure()
                    exploded_options = self._conanfile_wrapper.conjugate_options(recipe.options._data.keys())
                    for pack in exploded_options:
                        options_pack = {key: value for key, value in zip(recipe.options._data.keys(), pack)}
                        yield (compiler, items, options_pack)
                except ConanException:
                    log.info("Configuration not supported: os_system={}, compiler={}, {}".format(os_system, compiler.compiler, items))
                    pass

    def filter_jobs(self, filter):
        for it in self.enumerate_jobs():
            if not filter or filter(*it):
                yield it

    def paginate(self, page, page_size, filter=None):
        jobs = list(self.filter_jobs(filter=filter))
        init = page*page_size
        end = min((page+1)*page_size, len(jobs))
        return jobs[init:end]
