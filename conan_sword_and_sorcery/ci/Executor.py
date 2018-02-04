# -*- coding: utf-8 -*-

import os
import sys
import itertools
import logging
import platform
from collections import defaultdict
from operator import itemgetter
from conans.errors import ConanException
from conans.util.env_reader import get_env

from conan_sword_and_sorcery.parsers.conanfile import ConanfileWrapper
from conan_sword_and_sorcery.ci.settings import Settings
from conan_sword_and_sorcery.ci.compilers import CompilerRegistry, NoCompiler

log = logging.getLogger(__name__)


class Executor(object):
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

        log.debug(" - got filters: {}".format(filters))
        return filters

    def get_compilers(self):
        log.debug("Executor::get_compilers()")
        recipe_settings = self.recipe.settings._data.keys()
        if 'compiler' in recipe_settings:
            filters = self.get_filters_for_compilers(recipe_settings=self.recipe.settings._data.keys())
            return list(CompilerRegistry.get_compilers(**filters))
        else:
            return None

    def enumerate_jobs(self):
        log.debug("Executor::enumerate_jobs()")

        # Get compilers
        compilers = self.get_compilers()
        if compilers is not None:
            log.debug(" - got {} compilers: {}".format(len(compilers), compilers))

            for compiler in compilers:
                compiler.update_settings(self._settings)
                try:
                    self.recipe.configure()

                    # Enumerate options
                    exploded_options = self._conanfile_wrapper.conjugate_options(self.recipe.options._data.keys())
                    if not exploded_options:
                        yield (compiler, {})  # Empty dict for options.
                    else:
                        options = [{key: value for key, value in zip(self.recipe.options._data.keys(), pack)} for pack in exploded_options]
                        log.debug(" - got {} options combinations: {}".format(len(options), options))
                        for it in itertools.product([compiler, ], options):
                            yield it
                except ConanException as e:  # TODO: Something like ConanInvalidConfiguration would fit better
                    pass
        else:
            exploded_options = self._conanfile_wrapper.conjugate_options(self.recipe.options._data.keys())
            if not exploded_options:
                yield (NoCompiler(os=str(self._settings.os)), {})
            else:
                options = [{key: value for key, value in zip(self.recipe.options._data.keys(), pack)} for pack in exploded_options]
                compilers = [NoCompiler(os=str(self._settings.os)), ]
                log.debug(" - got {} options combinations: {}".format(len(options), options))
                for it in itertools.product(compilers, options):
                    yield it
        return

    def filter_jobs(self, filter):
        for compiler, options in self.enumerate_jobs():
            if not filter or filter(compiler, options):
                yield compiler, options

    def paginate(self, page, page_size, filter=None):
        jobs = list(self.filter_jobs(filter=filter))
        init = page*page_size
        end = min((page+1)*page_size, len(jobs))
        return jobs[init:end]


def print_jobs(all_jobs, printer=sys.stdout.write):
    compiler_headers_ext = set()
    option_headers = set()
    for compiler, options in all_jobs:
        compiler_headers_ext.update(compiler._data.keys())
        option_headers.update(options.keys())

    compiler_headers = ['id', 'version', 'arch', 'build_type']
    compiler_headers += [it for it in compiler_headers_ext if it not in compiler_headers]

    table = []
    for compiler, options in all_jobs:
        table.append([getattr(compiler, it, '') for it in compiler_headers] +
                     [options.get(it, '') for it in option_headers])

    if len(table):
        from tabulate import tabulate
        printer(tabulate(table, headers=list(compiler_headers)+list(option_headers),
                         # showindex=True,
                         tablefmt='psql'))
        printer("\n")
    else:
        sys.stdout.write("There are no jobs!\n")
