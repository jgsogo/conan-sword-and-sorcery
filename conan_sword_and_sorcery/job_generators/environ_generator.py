# -*- coding: utf-8 -*-

import os
from conans.util.env_reader import get_env

from conan_sword_and_sorcery.job_generators.base import JobGeneratorBase


class JobGeneratorEnviron(JobGeneratorBase):
    """ JobGenerator based on environment variables. By default it gets those from parent (all) """

    def _get_archs(self):  # type: () -> List[str]
        return get_env("CONAN_ARCHS", super(JobGeneratorEnviron, self)._get_archs())

    def _get_build_types(self):  # type: () -> List[str]
        return get_env("CONAN_BUILD_TYPES", super(JobGeneratorEnviron, self)._get_build_types())
