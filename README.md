Conan - Sword and Sorcery
=========================

[![coverage](https://gitlab.com/jgsogo/conan-sword-and-sorcery/badges/master/coverage.svg?job=coverage)](http://jgsogo.gitlab.io/conan-sword-and-sorcery/)
[![pipeline](https://gitlab.com/jgsogo/conan-sword-and-sorcery/badges/master/pipeline.svg)](https://gitlab.com/jgsogo/conan-sword-and-sorcery/commits/master)

> **Status**: beta version. Under development

Utilities for [Conan The Frogarian](https://conan.io). At this moment it addressed
following tasks for your conan recipes:

 * [Travis CI](https://travis-ci.org/) integration (with docker).
 * [Appveyor](http://www.appveyor.com/) integration.
 * Batch build for all local profiles.

This project is just a refurbish of [conan-package-tools](https://github.com/conan-io/conan-package-tools)
which is officially maintained by conan team.

To install, just type (or clone and install this repo):

```shell
$ pip install conan_sword_and_sorcery
```

Index
-----

 * [Batch build](#batch-builds): `run_ci`
   - [Local console](#local-console)
   - [Continuous integration systems](#continuous-integration-systems)
   - [Upload packages](#upload-packages)


Batch builds
------------

This is the main functionality, it allows you to build several configurations of
your recipe and your compiler using one single command `run_ci`. It can be used
from your local machine and from continuos integration systems:

```shell
$ run_ci --help
usage: run_ci [-h] [-v] [--dry-run] [--options CONAN_OPTIONS]
              [--username CONAN_USERNAME] [--channel CONAN_CHANNEL]
              conanfile

Run CI for given conanfile

positional arguments:
  conanfile             Path to conanfile.py

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increases log verbosity for each occurence.
  --dry-run             do not create package (won't compile recipes)
  --options CONAN_OPTIONS
                        comma separated list of options from de conanfile.py
                        to conjugate
  --username CONAN_USERNAME
                        Username for package reference
                        xxx/x.y.z@<username>/xxxx
  --channel CONAN_CHANNEL
                        Channel for package reference
                        xxx/x.y.z@xxxxxx/<channel>
```

After the compilation it will upload the packages if some conditions match (see below).

### Local console

When used from local console, it will look for all your profile files defined in your
`CONAN_USER_HOME/profiles` directory and trigger a build for them. If any options are
given it will explode those and generate all the available combinations, e.g.:

```shell
$ run_ci ..\conan-protobuf\conanfile.py --options=with_zlib,build_tests
=== Conan - Sword & Sorcery ===
All combinations sum up to 8 jobs
Jobs to run...
+---------------+-----------+--------+--------------+-----------+---------------+-------------+
| id            |   version | arch   | build_type   | runtime   | build_tests   | with_zlib   |
|---------------+-----------+--------+--------------+-----------+---------------+-------------|
| Visual Studio |        14 | x86_64 | Debug        | MDd       | True          | True        |
| Visual Studio |        14 | x86_64 | Debug        | MDd       | True          | False       |
| Visual Studio |        14 | x86_64 | Debug        | MDd       | False         | True        |
| Visual Studio |        14 | x86_64 | Debug        | MDd       | False         | False       |
| Visual Studio |        14 | x86_64 | Release      | MD        | True          | True        |
| Visual Studio |        14 | x86_64 | Release      | MD        | True          | False       |
| Visual Studio |        14 | x86_64 | Release      | MD        | False         | True        |
| Visual Studio |        14 | x86_64 | Release      | MD        | False         | False       |
+---------------+-----------+--------+--------------+-----------+---------------+-------------+

[...]
```

### Continuous integration systems

For CI systems jobs are driven using environment variables, same as conan-package-tools,
so your existing `appveyor.yml` and `.travis.yml` files should work out of the box
after installing this package and changing the execution line for the `run_ci` one.

Available environment variables are:

 * `CONAN_USERNAME`
 * `CONAN_CHANNEL`
 * `CONAN_REMOTES`: comma separated list of additional remotes to look for dependencies
 * `CONAN_OPTIONS`: comma separated list of options, `run_ci` will explode all its
   combinations and perform those builds.
 * `CONAN_BUILD_PACKAGES`: comma separated list of dependencies to build from source.
 * For compilers (only meaningful combinations build be generated):
   - `CONAN_ARCHS`: architectures to build for, comma separated, e.g.: "x86,x86_64"
   - `CONAN_BUILD_TYPES`: comma separated, e.g.: "Release,Debug"
   - gcc:
     + `CONAN_GCC_VERSIONS`: comma separated, e.g.: "4.9,5,7"
   - Visual Studio:
     + `CONAN_VISUAL_VERSIONS`: comma separated, e.g.: "12,14"
     + `CONAN_VISUAL_RUNTIMES`: comma separated, e.g.: "MT, MD"
   - clang:
     + `CONAN_CLANG_VERSIONS`: comman separated, e.g.: "4.0,5.0"
   - apple-clang:
     + `CONAN_APPLE_CLANG_VERSIONS`: comman separated, e.g.: "8.1,9.0"
 * Specific to Travis CI:
   - Travis CI supports dockerized builds, so it will look for `CONAN_DOCKER_IMAGE`
     env variable and run compilations inside it. If no docker image is specified, but
     it is set `CONAN_USE_DOCKER=True` the the corresponding image to the compiler will
     be used from @lasote available ones (see [list here](https://github.com/conan-io/conan-docker-tools)).


### Upload packages

After a successful `run_ci` execution it will try to upload the generated packages if
some conditions are satisfied:

 * `CONAN_UPLOAD_ONLY_WHEN_STABLE`: will try to upload only if the channel is stable
 * `CONAN_STABLE_BRANCH_PATTERN` (regex): determine if the repository branch is stable,
   by default it is true for any given branch that follows a pattern like `stable/v1.2.3`,
   `stable/1.2rc2.dev32`,... ([more](./tests/test_ci/test_runners/test_StableBranchPattern.py)).
 * `CONAN_LOGIN_USERNAME` (defaults to `CONAN_USERNAME`).
 * `CONAN_UPLOAD`: URL of the repository to upload packages to (it also will be used as
   a remote for dependencies).
 * `CONAN_PASSWORD`: password to authenticate in the repository

