# -*- coding: utf-8 -*-

import os
import logging

from conans.model.settings import Settings as ConanSettings

log = logging.getLogger(__name__)


class Settings(object):
    # TODO: Remove this class a work just with conan_settings

    @classmethod
    def default(cls):
        filename = os.path.join(os.path.dirname(__file__), '..', 'conan_settings.yaml')  # TODO: Use conan_sword_and_sorcery distributed one as default.
        with open(filename, 'r') as f:
            return ConanSettings.loads(f.read())

    def __init__(self, settings_filename=None):
        if settings_filename:
            with open(settings_filename, 'r') as f:
                self.conan_settings = ConanSettings.loads(f.read())
        else:
            self.conan_settings = Settings.default()

