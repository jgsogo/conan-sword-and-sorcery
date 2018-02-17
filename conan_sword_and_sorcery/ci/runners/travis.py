# -*- coding: utf-8 -*-

import logging

from .base_runner import BaseRunner
from .registry import RunnerRegistry
from ._docker import DockerMixin

log = logging.getLogger(__name__)


@RunnerRegistry.register("TRAVIS")
class TravisRunner(DockerMixin, BaseRunner):
    pass


