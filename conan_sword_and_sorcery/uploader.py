# -*- coding: utf-8 -*-

import os
import logging
from conan_sword_and_sorcery.utils import conan
from conan_sword_and_sorcery.utils.cmd import cmd

log = logging.getLogger(__name__)


def upload(recipe, username, channel, dry_run=False):
    # TODO: Check requirements in a free function so it can be called before it all starts.
    # Check requirements:
    LOGIN_USERNAME = os.getenv("CONAN_LOGIN_USERNAME", os.getenv("CONAN_USERNAME", None))
    REMOTE = os.getenv("CONAN_UPLOAD", False)
    PASSWORD = os.getenv("CONAN_PASSWORD", None)
    if not REMOTE:
        log.error("No remote provided in 'CONAN_UPLOAD' env variable")
        return
    if not PASSWORD or not LOGIN_USERNAME:
        raise ValueError("No password or username provided for remote '{}'. Use env variable 'CONAN_PASSWORD' and 'CONAN_LOGIN_USERNAME' to provide them.".format(REMOTE))

    # Add remote and upload
    log.info("Add conan remote: {url}".format(url=REMOTE))
    with conan.remote(url=REMOTE) as remote_name:
        log.info("Authenticate user '{username}' in remote {url}".format(username=LOGIN_USERNAME, url=REMOTE))
        conan.remote_auth(remote_name, LOGIN_USERNAME, PASSWORD)

        # Upload command
        package_ref = "{}/{}@{}/{}".format(recipe.name, recipe.version, username, channel)
        command = "conan upload -r {} --all --force --confirm {}".format(remote_name, package_ref)  # TODO: Need 'sudo' because the packages may have been created using another user (inside docker). Fix this, how?
        if not dry_run:
            cmd(command)
