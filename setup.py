#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='rdbms_anonymize',
    version='0.1.0',
    description="Anonymize relational database by replacing PII with fake data",
    long_description=readme + '\n\n' + history,
    author="18F",
    author_email='catherine.devlin@gsa.gov',
    url='https://github.com/18F/rdbms_anonymize',
    packages=[
        'rdbms_anonymize',
    ],
    package_dir={'rdbms_anonymize':
                 'rdbms_anonymize'},
    entry_points={
        'console_scripts': [
            'rdbms_anonymize=rdbms_anonymize.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="CC0 license",
    zip_safe=False,
    keywords='rdbms_anonymize',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
