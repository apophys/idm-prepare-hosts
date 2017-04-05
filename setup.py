#!/usr/bin/env python

from setuptools import setup, find_packages
import io


with io.open("README.md") as f:
    long_description = f.read()

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Topic :: Utilities'
]

VERSION = '0.0.1'

args = dict(
    name='ipaqe-provision-hosts',
    version=VERSION,
    author='FreeIPA QA',
    author_email='mkubik@redhat.com',
    url='https://github.com/apophys/ipaqe-provision-hosts',
    description=(
        'Command line utility for FreeIPA multihost environment preparation'
    ),
    long_description=long_description,
    license='MIT',
    classifiers=CLASSIFIERS,

    packages=find_packages(),
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
