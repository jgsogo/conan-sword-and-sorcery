# -*- coding: utf-8 -*-

import os
import logging
import uuid

log = logging.getLogger(__name__)


class Uploader(object):

    def __init__(self, recipe, username, channel, dry_run=False):
        self.username = username
        self.package = "{}/{}".format(recipe.name, recipe.version)
        self.reference = "{}/{}".format(username, channel)
        self.dry_run = dry_run

    @classmethod
    def requested(cls):
        return bool(os.getenv("CONAN_UPLOAD", False))

    def upload(self, remote):
        remote_name = uuid.uuid4()
        # Add remote
        command = "conan remote add {name} {url} --insert 0".format(name=remote_name, url=remote)
        log.info("Uploader command: {}".format(command))
        if not self.dry_run:
            r = os.system(command)
            if r != 0:
                raise RuntimeError("Error adding remote")

        # Authenticate remote
        command = "conan user -p {{password}} -r {remote} {username}".format(
            username=self.username,
            remote=remote_name,
        )
        log.info("Uploader command: {}".format(command))
        if not self.dry_run:
            password = os.getenv("CONAN_PASSWORD", None)  # TODO: Gather all envs together
            if not password:
                raise RuntimeError("Provide a 'CONAN_PASSWORD' to upload to remote")
            command = command.format(password=password)  # Keep password outside log
            r = os.system(command)
            if r != 0:
                raise RuntimeError("Erorr authenticating user '{}' in remote '{}'".format(self.username, remote_name))

        # Upload command
        command = "conan upload -r {remote} --all --force --confirm {package}@{reference}".format(
            remote=remote_name,
            package=self.package,
            reference=self.reference,
        )
        log.info("Uploader command: {}".format(command))
        if not self.dry_run:
            r = os.system(command)
            if r != 0:
                raise RuntimeError("Error in upload command")

