# -*- coding: utf-8 -*-

import tempfile
import logging
import os

log = logging.getLogger(__name__)


class JobRunner(object):

    def profile_file(self):
        tmp

    def run(self, compiler, options):



class JobRunnerAppVeyor(JobRunner):
    # There is no docker option
    pass


class JobRunnerAppVeyor(JobRunner):
    # There is no docker option
    pass


def get_runner():
    travis = os.getenv("TRAVIS", False)
    appveyor = os.getenv("APPVEYOR", False)
    circleci = os.getenv("CIRCLECI", False)
    gitlab = os.getenv("GITLAB_CI", False)



def run_job(compiler, options):
    # Within a profile tmp file
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write("include(default)\n\n") # Profile 'default'
        tmp.write("[settings]\n")
        compiler.populate_profile_settings(tmp)
        tmp.write("[options]\n[build_requires]\n[env]\n")  # TODO: Is it needed?

        # Get proper runner
        runner = JobRunnerAppVeyor(profile=tmp.name)
        ret = runner.run(compiler, options)
