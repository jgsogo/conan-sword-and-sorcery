# -*- coding: utf-8 -*-

from .base_runner import BaseRunner
from .registry import RunnerRegistry


@RunnerRegistry.register("APPVEYOR")
class AppveyorRunner(BaseRunner):
    pass

