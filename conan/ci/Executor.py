# -*- coding: utf-8 -*-

import itertools
import logging
from operator import itemgetter
from conans.errors import ConanException

from .settings import get_settings
from conan.parsers.conanfile import ConanfileWrapper
from conan.ci.settings import Settings

log = logging.getLogger(__name__)


class Executor:
    def __init__(self, conanfile, os_system=None):
        log.debug("Executor::__init__(conanfile='{}', os_system='{}')".format(conanfile, os_system))
        self._settings = Settings()
        self._conanfile_wrapper = ConanfileWrapper.parse(conanfile)

    def enumerate_jobs(self):
        log.debug("Executor::enumerate_jobs")

        # Get all compilers and configurations available for this operating system
        settings_to_run = get_settings()

        # Group settings by compiler and iterate
        for compiler, group in itertools.groupby(settings_to_run, itemgetter(1)):
            for os_system, compiler, items in group:
                log.debug(" - set_current({}, {}, {})".format(os_system, compiler.compiler, items))
                s = self._settings.current(os_system, compiler, **items)
                recipe = self._conanfile_wrapper.recipe_class(output=None, runner=None, settings=s)
                try:
                    recipe.configure()
                    exploded_options = self._conanfile_wrapper.conjugate_options(recipe.options._data.keys())
                    for pack in exploded_options:
                        options_pack = {key: value for key, value in zip(recipe.options._data.keys(), pack)}
                        yield (os_system, compiler, items, options_pack)
                except ConanException:
                    log.info("Configuration not supported: os_system={}, compiler={}, {}".format(os_system, compiler.compiler, items))
                    pass
