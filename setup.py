#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='mute',
    version=0.1,
    description='ubuntu mute',
    url='https://github.com/sovrin-foundation/sovrin-client.git',
    author='Jason Law',
    license="Apache 2.0",
    packages=find_packages(),
    package_data={'': ['LICENSE', '*.png']},
    include_package_data=True,
    install_requires=[],
    setup_requires=[],
    tests_require=[],
    scripts=['scripts/mute', 'scripts/shortcut']
)
