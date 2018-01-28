# -*- coding: utf-8 -*-


import platform


class RunHelper:
    """
    Wrapper to access environment variables and configuration for each CI system
    """

    @property
    def os(self):
        return platform.system()

