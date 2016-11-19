#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2016, Oz Tiram <oz.tiram@mobilityhouse.com>
"""
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))


setup(
    name='bcc',
    version="0.0.1",
    description="none yes",
    long_description=open("README.rst").read(),
    author='Oz Tiram',
    author_email='oz.tiram@mobilityhouse.com',
    url="https://github.com/mobilityhouse/bcc",
    license='',
    classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Programming Language :: Python'
    ],
    zip_safe=False,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    install_requires=[""],
    tests_require=["pytest", "webtest"],
    cmdclass={'test': PyTest},
)

