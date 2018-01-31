# -*- coding: utf-8 -*-

import os
import itertools
import logging
import platform
from collections import defaultdict
from operator import itemgetter
from conans.errors import ConanException
from conans.util.env_reader import get_env

from conan.parsers.conanfile import ConanfileWrapper
from conan.ci.settings import Settings
from conan.ci.compilers import CompilerRegistry, NoCompiler

log = logging.getLogger(__name__)


class Executor:
    def __init__(self, conanfile, osys=platform.system()):
        log.debug("Executor::__init__(conanfile='{}', osys='{}')".format(conanfile, osys))
        self._settings = Settings.default()
        self._conanfile_wrapper = ConanfileWrapper.parse(conanfile)

        # Set settings
        self._settings.os = osys
        self.recipe = self._conanfile_wrapper.recipe_class(output=None, runner=None, settings=self._settings)

    def get_filters_for_compilers(self, recipe_settings):
        log.debug("Executor::get_filters_for_compilers()")
        filters = {}

        if 'os' in recipe_settings:
            filters['os'] = [str(self._settings.os), ]

        if 'compiler' in recipe_settings:
            filters['version'] = []

            # Helper function to avoid duplication getting values from env variable
            def _populate_filters(key, env_var, default=None):
                if key in recipe_settings:
                    filters[key] = get_env(env_var, getattr(self._settings, key).values_range)
                else:
                    filters[key] = default or getattr(self._settings, key).values_range[0]  # TODO: Choose the best one

            _populate_filters('arch', "CONAN_ARCHS")
            _populate_filters('build_type', "CONAN_BUILD_TYPES")

            # Get all filters related to compilers (versions, runtimes,...)
            env_filters = CompilerRegistry.environment_filters()
            filters.update(env_filters)

        else:
            # If recipe does not depend on compiler, use "no-compiler" to get one run
            filters['version'] = [(NoCompiler.id, ''), ]
        log.debug(" - got filters: {}".format(filters))
        return filters

    def get_compilers(self):
        log.debug("Executor::get_compilers()")
        filters = self.get_filters_for_compilers(recipe_settings=self.recipe.settings._data.keys())
        return CompilerRegistry.get_compilers(**filters)

    def enumerate_jobs(self):
        log.debug("Executor::enumerate_jobs()")

        # Get compilers
        compilers = list(self.get_compilers())
        log.debug(" - got {} compilers: {}".format(len(compilers), compilers))

        # Enumerate options
        exploded_options = self._conanfile_wrapper.conjugate_options(self.recipe.options._data.keys())
        if not exploded_options:
            for compiler in compilers:
                yield (compiler, {})  # Empty dict for options.
        else:
            options = [{key: value for key, value in zip(self.recipe.options._data.keys(), pack)} for pack in exploded_options]
            log.debug(" - got {} options combinations: {}".format(len(options), options))
            for it in itertools.product(compilers, options):
                yield it


    def filter_jobs(self, filter):
        for it in self.enumerate_jobs():
            if not filter or filter(*it):
                yield it

    def paginate(self, page, page_size, filter=None):
        jobs = list(self.filter_jobs(filter=filter))
        init = page*page_size
        end = min((page+1)*page_size, len(jobs))
        return jobs[init:end]
