# -*- coding: utf-8 -*-

import os
import logging

from conans.model.settings import Settings
from conans.client.conf import default_settings_yml

log = logging.getLogger(__name__)


def get_settings(filename=None):
    if filename:
        with open(filename, 'r') as f:
            return Settings.loads(f.read())
    else:
        return Settings.loads(default_settings_yml)
