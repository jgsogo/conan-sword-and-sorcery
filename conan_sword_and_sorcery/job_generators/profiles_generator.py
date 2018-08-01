# -*- coding: utf-8 -*-

import logging
import os

from conan_sword_and_sorcery.ci.compilers import CompilerRegistry
from conan_sword_and_sorcery.job_generators.base import JobGeneratorBase
from conan_sword_and_sorcery.parsers.profile import parse_profile

log = logging.getLogger(__name__)


class JobGeneratorProfiles(JobGeneratorBase):
    """ JobGenerator based on profile files in local machine """

    def _get_compilers(self, recipe_settings_keys):
        log.debug("JobGeneratorProfiles::get_compilers(recipe_settings_keys='{}')".format(', '.join(recipe_settings_keys)))
        # TODO: Get from CONAN_USER_HOME
        profiles_dirname = os.path.join(os.path.expanduser("~"), '.conan', 'profiles')
        # TODO: Check for duplicate files (equal content configuration)
        # TODO: How to handle options for child packages?
        for filename in os.listdir(profiles_dirname):
            log.debug(" - parse profile file '{}'".format(filename))
            data = parse_profile(os.path.join(profiles_dirname, filename))
            filters = {key: [data['settings'][key], ] for key in recipe_settings_keys if key not in ['compiler', 'os', ]}
            for item, value in data.items():
                if item.startswith('compiler.') and not item.endswith('version'):
                    filters[item.split('.')[1]] = [value, ]
            version = [(data['compiler'], data['compiler.version']), ]

            compilers = list(CompilerRegistry.get_compilers(os=data['os'], version=version, **filters))
            assert len(compilers) == 1

            yield compilers[0]
