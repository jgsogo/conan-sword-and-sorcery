# -*- coding: utf-8 -*-

import itertools
import logging
from operator import itemgetter

from .settings import get_settings
from conan.parsers.conanfile import ConanfileWrapper
from conan.ci.settings import Settings

log = logging.getLogger(__name__)


class Executor(object):

    def __init__(self, conanfile, os_system=None):
        log.debug("Executor::__init__(conanfile='{}', os_system='{}')".format(conanfile, os_system))
        self._settings = Settings()
        self._conanfile_wrapper = ConanfileWrapper.parse(conanfile)

    def enumerate_jobs(self):
        log.debug("Executor::enumerate_jobs")
        # Group settings by compiler
        settings_to_run = get_settings()
        for compiler, group in itertools.groupby(settings_to_run, itemgetter(1)):
            for os_system, compiler, items in group:
                log.debug(" - set_current({}, {}, {})".format(os_system, compiler.compiler, items))
                s = self._settings.current(os_system, compiler, **items)
                recipe = self._conanfile_wrapper.recipe_class(output=None, runner=None, settings=s)
                recipe.configure()
