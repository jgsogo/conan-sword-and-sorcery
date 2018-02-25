# -*- coding: utf-8 -*-
import itertools
import logging

from conans.errors import ConanException
from conans.model.settings import Settings

from conan_sword_and_sorcery.ci.compilers import CompilerRegistry, NoCompiler
from conan_sword_and_sorcery.parsers.conanfile import ConanFileWrapper

log = logging.getLogger(__name__)


class JobGeneratorBase(object):
    def __init__(self, conanfile_wrapper, settings, osys):  # type: (ConanFileWrapper, Settings, str) -> None
        log.debug("JobGenerator::__init__(conanfile_wrapper='{}', settings='{}', osys='{}')".format(conanfile_wrapper, settings, osys))
        self._settings = settings
        self._conanfile_wrapper = conanfile_wrapper

        # Instantiate recipe with settings
        self._settings.os = osys
        self._conanfile_wrapper.instantiate(settings=self._settings)

    def _get_archs(self):  # type: () -> List[str]
        try:
            return getattr(self._settings, 'arch').values_range
        except KeyError:
            return getattr(self._settings, 'arch').values_range[0]  # TODO: Choose the best one (any will work?)

    def _get_build_types(self):  # type: () -> List[str]
        try:
            return getattr(self._settings, 'build_type').values_range
        except KeyError:
            return getattr(self._settings, 'build_type').values_range[0]  # TODO: May return None?

    def _get_options_to_conjugate(self):  # type: () -> List[str]
        return []  # TODO: None by default (or should I default to all of them?

    def _get_filters_for_compilers(self, recipe_settings_keys):  # type: (List[str]) -> Dict[str, List[str]]
        log.debug("Executor::get_filters_for_compilers()")
        filters = {}

        if 'os' in recipe_settings_keys:
            filters['os'] = [str(self._settings.os), ]
        if 'arch' in recipe_settings_keys:
            filters['arch'] = self._get_archs()
        if 'build_type' in recipe_settings_keys:
            filters['build_type'] = self._get_build_types()

        # filters['version'] = []  # TODO Is it needed?

        # Get all filters related to compilers (versions, runtimes,...)
        env_filters = CompilerRegistry.environment_filters()
        filters.update(env_filters)

        log.debug(" - got filters: {}".format(filters))
        return filters

    def _get_compilers(self, recipe_settings_keys):
        log.debug("Executor::get_compilers(recipe_settings_keys='{}')".format(', '.join(recipe_settings_keys)))
        if 'compiler' in recipe_settings_keys:
            filters = self._get_filters_for_compilers(recipe_settings_keys=recipe_settings_keys)
            return list(CompilerRegistry.get_compilers(**filters))
        else:
            log.debug(" - no 'compiler' in recipe settings")
            return None

    def _get_exploded_options(self):
        # Enumerate (and filter) options
        options_to_conjugate = set(self._conanfile_wrapper.options._data.keys())
        options_to_conjugate = options_to_conjugate.intersection(set(self._get_options_to_conjugate()))

        # Explode options
        exploded_options = self._conanfile_wrapper.conjugate_options(options_to_conjugate)
        if exploded_options:
            options = [{key: value for key, value in zip(options_to_conjugate, pack)} for pack in exploded_options]
            return options
        return None

    def enumerate_jobs(self):
        log.debug("Executor::enumerate_jobs()")

        # Get compilers
        compilers = self._get_compilers(recipe_settings_keys=self._conanfile_wrapper.settings._data.keys())
        if compilers is not None:
            log.debug(" - got {} compilers: {}".format(len(compilers), compilers))

            for compiler in compilers:
                compiler.update_settings(self._settings)
                try:
                    self._conanfile_wrapper.configure()  # Check if settings configuration is supported

                    options = self._get_exploded_options()
                    if not options:
                        yield (compiler, {})  # Empty dict for options.
                    else:
                        log.debug(" - got {} options combinations: {}".format(len(options), options))
                        for compiler, option_pack in itertools.product([compiler, ], options):
                            for k, v in option_pack.items():
                                setattr(self._conanfile_wrapper.options, k, v)
                            try:
                                self._conanfile_wrapper.configure()
                                yield compiler, option_pack
                            except ConanException as e:  # TODO: Something like ConanInvalidConfiguration would fit better
                                # TODO: Inform the client about the reason to skip this combination
                                pass

                except ConanException as e:  # TODO: Something like ConanInvalidConfiguration would fit better
                    # TODO: Inform the client about the reason to skip this combination
                    pass
        else:
            options = self._get_exploded_options()
            if not options:
                yield (NoCompiler(os=str(self._settings.os)), {})
            else:
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
