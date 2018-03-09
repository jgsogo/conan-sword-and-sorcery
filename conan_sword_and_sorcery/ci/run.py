# -*- coding: utf-8 -*-

import argparse
import logging
import os
import platform
import sys
from itertools import groupby
from operator import itemgetter

try:
    from contextlib import ExitStack
except ImportError:
    from contextlib2 import ExitStack

from conans.util.env_reader import get_env
from conan_sword_and_sorcery.utils import slice, conan
from conan_sword_and_sorcery.job_generators.printer import print_jobs
from conan_sword_and_sorcery.ci.runners import RunnerRegistry
from conan_sword_and_sorcery.ci.runners.base_runner import SUCCESS
from conan_sword_and_sorcery.parsers.profile import profile_for
from conan_sword_and_sorcery.parsers.settings import get_settings
from conan_sword_and_sorcery.job_generators import JobGeneratorBase
from conan_sword_and_sorcery.utils.environ import context_env

log = logging.getLogger('conan_sword_and_sorcery')


class CLIFormatter(logging.Formatter):
    max_length = 10

    def format(self, record):
        name = record.__dict__['name'].split('.', 1)[1]
        record.name = '~.{}'.format(name)
        return super(CLIFormatter, self).format(record)


def main():
    sys.stdout.write("=== Conan - Sword & Sorcery ===\n")

    parser = argparse.ArgumentParser(description='Run CI for given conanfile')
    parser.add_argument('conanfile', help='Path to conanfile.py')
    parser.add_argument("-v", "--verbose", dest="verbose_count",
                        action="count", default=0,
                        help="increases log verbosity for each occurence.")
    parser.add_argument("--dry-run", dest="dry_run",
                        action='store_true', default=False,
                        help="do not create package (won't compile recipes)")
    parser.add_argument("--options", dest="conan_options",
                        help="comma separated list of options from de conanfile.py to conjugate")
    parser.add_argument("--username", dest="conan_username",
                        help="Username for package reference xxx/x.y.z@<username>/xxxx")
    parser.add_argument("--channel", dest="conan_channel",
                        help="Channel for package reference xxx/x.y.z@xxxxxx/<channel>")
    args = parser.parse_args()

    # Configure logging
    my_formatter = CLIFormatter('[%(levelname)-8s] %(name)-36s (%(lineno)d): %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(my_formatter)
    # logging.basicConfig(stream=sys.stderr, level=logging.INFO,
    #                    format='[%(levelname)-8s] %(name)s (%(lineno)d): %(message)s')
    log.setLevel(max(3 - args.verbose_count, 0) * 10)
    log.addHandler(handler)

    # Check that the file exists
    conanfile = os.path.abspath(args.conanfile)
    if not os.path.exists(conanfile):
        sys.stderr.write("Conanfile '{}' does not exists or it is inaccessible\n".format(conanfile))
        exit(-1)

    # May override environament (options) from command line
    env_vars = {}
    if args.conan_options:
        log.info("Override 'CONAN_OPTIONS' env variable with '{}'".format(args.conan_options))
        env_vars["CONAN_OPTIONS"] = args.conan_options
    if args.conan_username:
        log.info("Override 'CONAN_USERNAME' env variable with '{}'".format(args.conan_username))
        env_vars["CONAN_USERNAME"] = args.conan_username
    if args.conan_channel:
        log.info("Override 'CONAN_CHANNEL' env variable with '{}'".format(args.conan_channel))
        env_vars["CONAN_CHANNEL"] = args.conan_channel

    with context_env(**env_vars):
        r = run(conanfile=conanfile, dry_run=args.dry_run)

    sys.stdout.write("=====\n")
    return r


def run(conanfile, filter_func=None, dry_run=False):
    # Do the work
    osys = platform.system()
    if osys == "Darwin":
        osys = "Macos"

    # Look for runner
    runner = RunnerRegistry.get_runner(conanfile=conanfile, settings=get_settings(), osys=osys, dry_run=dry_run)
    all_jobs = runner.enumerate_jobs()
    all_jobs = list(JobGeneratorBase.filter_jobs(all_jobs, filter=filter_func))
    sys.stdout.write("All combinations sum up to {} jobs\n".format(len(all_jobs)))

    # - may paginate
    total_pages = os.environ.get("CONAN_TOTAL_PAGES", None)
    current_page = os.environ.get("CONAN_CURRENT_PAGE", None)
    msg = ''
    if total_pages or current_page:
        assert total_pages and current_page, "Both environment variables must be set: CONAN_TOTAL_PAGES and CONAN_CURRENT_PAGE"
        init, end = slice(len(all_jobs), int(current_page), int(total_pages))
        all_jobs = all_jobs[init:end]
        msg = "(page {}/{})".format(current_page, total_pages)

    # Print jobs to run
    sys.stdout.write("Jobs to run... {}\n".format(msg))
    print_jobs(all_jobs)
    results = []

    # Get username and channel
    USERNAME = os.getenv("CONAN_USERNAME", 'conan')
    CHANNEL = os.getenv("CONAN_CHANNEL", 'stable' if runner.is_stable_branch() else 'testing')

    # Aggregate jobs by compiler and iterate
    grouped_jobs = groupby(all_jobs, itemgetter(0))
    i = 0
    total = len(all_jobs)

    with ExitStack() as stack:
        # Add remotes in order of precedence
        ADDITIONAL_REMOTES = get_env("CONAN_REMOTES", [])
        for remote in reversed(ADDITIONAL_REMOTES):
            _ = stack.enter_context(conan.remote(url=remote))

        REMOTE = os.getenv("CONAN_UPLOAD", None)
        if REMOTE and REMOTE not in ADDITIONAL_REMOTES:
            _ = stack.enter_context(conan.remote(url=REMOTE))

        # Run jobs
        for compiler, options in grouped_jobs:
            # Get a runner for each compiler (will modify profile)
            runner.set_compiler(compiler)
            with profile_for(compiler) as profile_file:
                runner.set_profile(profile_file)
                for _, opt in options:
                    i += 1
                    options_str = ["{}={}".format(key, value) for key, value in opt.items()]
                    sys.stdout.write("\n==> [{:>2}/{}] {}: {}\n".format(i, total, str(compiler), ', '.join(options_str)))
                    ret = runner.run(opt, username=USERNAME, channel=CHANNEL)
                    sys.stdout.write(ret + '\n\n')
                    results.append(ret)

    # Summary of jobs status
    sys.stdout.write("Summing up... {}\n".format(msg))
    print_jobs(all_jobs, job_status=results)

    succeed = len(results) == results.count(SUCCESS)
    if not succeed:
        sys.stdout.write("Only {} out of {} jobs succeeded (status={}) :/ \n\n".format(results.count(SUCCESS), len(results), SUCCESS))
        if not dry_run:
            return -1
    else:
        sys.stdout.write("All jobs succeeded!\n\n")

    # Upload (will raise if errors)
    runner.upload(USERNAME, CHANNEL)
    return 0 if succeed else -1


if __name__ == '__main__':
    main()
