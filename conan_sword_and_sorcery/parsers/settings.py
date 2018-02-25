# -*- coding: utf-8 -*-

import os
import logging

from conans.model.settings import Settings

log = logging.getLogger(__name__)


def get_settings(filename=None):
    filename = filename or os.path.join(os.path.expanduser("~"), '.conan', 'settings.yml')
    # filename = filename or os.path.join(os.path.dirname(__file__), '..', 'conan_settings.yaml')  # TODO: Use conan_sword_and_sorcery distributed one as default.
    with open(filename, 'r') as f:
        return Settings.loads(f.read())
