#!/usr/bin/env python

from setuptools import setup, find_packages

LONG_DESCRIPTION = """
The script reads a topology template specifying a domain for
the ipa installation and creating a configuration file for
the multihost tests with the provisioned resources.
"""


CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Topic :: Utilities'
]

VERSION = '0.1.0'

args = dict(
    name='ipaqe-provision-hosts',
    version=VERSION,
    author='FreeIPA QA',
    author_email='mkubik@redhat.com',
    url='https://github.com/apophys/ipaqe-provision-hosts',
    description=(
        'Command line utility for FreeIPA multihost environment preparation'
    ),
    long_description=LONG_DESCRIPTION,
    license='MIT',
    classifiers=CLASSIFIERS,

    packages=find_packages(exclude=['tests']),
    install_requires=[
        'PyYAML'
    ],

    entry_points={
        'console_scripts': [
            'ipaqe-provision-hosts=ipaqe_provision_hosts.__main__:main'
        ],
        'ipaqe_provision_hosts.backends': [
            'dummy = ipaqe_provision_hosts.backend.dummy:DummyBackend'
        ]
    }
)

setup(**args)
