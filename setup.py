# -*- coding: utf-8 -*-

import codecs

from setuptools import setup


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='El Cuestionario',
    version='0.4.1',
    description='A tiny web application to display and evaluate single-page questionnaires',
    long_description=long_description,
    url='http://homework.nwsnet.de/releases/8909/#el-cuestionario',
    author='Jochen Kupperschmidt',
    author_email='homework@nwsnet.de',
    license='GPLv2',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Games/Entertainment',
    ],
    packages=['elcuestionario'],
    install_requires=['flask>=0.10.1'],
    tests_require=['nose2'],
    test_suite='nose2.collector.collector',
    entry_points={
        'console_scripts': [
            'elcuestionario=runserver:main',
        ],
    },
)
