
import os
import re
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def get_long_description():
    return codecs.open(os.path.join(here, 'README.md'), encoding='utf-8').read()


def get_requirements(filename):
    with codecs.open(filename) as f:
        return list([line.strip() for line in f.readlines() if not line.startswith(("#", "-r"))])


def get_version():
    file_with_version = os.path.join(here, 'conan_sword_and_sorcery', '__init__.py')
    with codecs.open(file_with_version, "rt") as f:
        return re.search("__version__ = '([0-9a-z.]+)'", f.read()).group(1)


setup(
    name='conan_sword_and_sorcery',
    version=get_version(),
    long_description=get_long_description(),
    description="Utilities to work with conan.io stuf",
    url='https://gitlab.com/jgsogo/conan-sword-and-sorcery',
    author='jgsogo',
    author_email='jgsogo@gmail.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords=['conan', 'C/C++', 'package', 'libraries', 'developer', 'manager',
              'dependency', 'tool', 'c', 'c++', 'cpp'],

    packages=find_packages(exclude=['tests']),
    install_requires=get_requirements(os.path.join(here, 'requirements.txt')),

    # $ pip install -e .[dev,test]
    extras_require={
        'test': get_requirements(os.path.join(here, 'tests', 'requirements.txt'))
    },

    # package_data= Forget about it and use MANIFEST.in (http://blog.codekills.net/2011/07/15/lies,-more-lies-and-python-packaging-documentation-on--package_data-/)
    include_package_data=True,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'run_ci=conan_sword_and_sorcery.ci.run:main',
        ],
    },
)
