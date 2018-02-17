# -*- coding: utf-8 -*-

import os
import sys
import argparse
import logging
from itertools import groupby
from operator import itemgetter

from conan_sword_and_sorcery.ci.job_generator import JobGenerator, print_jobs
from conan_sword_and_sorcery.ci.runners import RunnerRegistry
from conan_sword_and_sorcery.utils import slice
from conan_sword_and_sorcery.profile import profile_for

log = logging.getLogger(__name__)


def run(filter_func=None):
    sys.stdout.write("=== Conan - Sword & Sorcery ===\n")

    parser = argparse.ArgumentParser(description='Run CI for given conanfile')
    parser.add_argument('conanfile', help='Path to conanfile.py')
    parser.add_argument("-v", "--verbose", dest="verbose_count",
                        action="count", default=0,
                        help="increases log verbosity for each occurence.")
    parser.add_argument("--dry-run", dest="dry_run",
                        action='store_true', default=False,
                        help="do not create package (won't compile recipes)")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(stream=sys.stderr, level=logging.INFO,
                        format='%(name)s (%(levelname)s): %(message)s')
    log.setLevel(max(3 - args.verbose_count, 0) * 10)

    # Check that the file exists
    conanfile = os.path.abspath(args.conanfile)
    if not os.path.exists(conanfile):
        sys.stderr.write("Conanfile '{}' does not exists or it is inaccessible\n".format(conanfile))
        exit(-1)

    # Do the work
    job_generator = JobGenerator(conanfile=conanfile)
    all_jobs = list(job_generator.filter_jobs(filter=filter_func))
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

    # Aggregate jobs by compiler and iterate
    grouped_jobs = groupby(all_jobs, itemgetter(0))
    i = 0
    for compiler, options in grouped_jobs:
        # Get a runner for each compiler (will modify profile)
        runner = RunnerRegistry.get_runner(compiler=compiler, conanfile=conanfile,
                                           recipe=job_generator.recipe, dry_run=args.dry_run)
        with profile_for(compiler) as profile_file:
            runner.set_profile(profile_file)
            for _, opt in options:
                i += 1
                options_str = ["{}={}".format(key, value) for key, value in opt.items()]
                sys.stdout.write("\n==> [{:>2}/{}] {}: {}\n".format(i, len(all_jobs), str(compiler), ', '.join(options_str)))
                ret = runner.run(opt)
                results.append(ret)

    # Summary of jobs status
    sys.stdout.write("\nSumming up... {}\n".format(msg))
    print_jobs(all_jobs, job_status=results)


if __name__ == '__main__':
    run()
