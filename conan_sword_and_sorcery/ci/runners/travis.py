# -*- coding: utf-8 -*-

from .base_runner import BaseRunner
from .registry import RunnerRegistry


@RunnerRegistry.register("TRAVIS")
class TravisRunner(BaseRunner):
    pass

