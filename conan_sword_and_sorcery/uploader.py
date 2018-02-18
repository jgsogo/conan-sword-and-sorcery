# -*- coding: utf-8 -*-

import os
import logging

log = logging.getLogger(__name__)


class Uploader(object):

    def __init__(self, recipe, username, channel, dry_run=False):
        self.package = "{}/{}".format(recipe.name, recipe.version)
        self.reference = "{}/{}".format(username, channel)
        self.dry_run = dry_run

    def upload(self):
        command = "conan upload -r {remote} --all {package}@{reference}".format(
            remote=self.remote,
            package=self.package,
            reference=self.reference,
        )
        log.info("Uploader command: {}".format(command))
        if not self.dry_run:
            r = os.system(command)
            if r != 0:
                raise RuntimeError("Error in upload command")
        
