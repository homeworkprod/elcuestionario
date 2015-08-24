#!/usr/bin/env python

from setuptools import setup


setup(
    name='El Cuestionario',
    version='0.4',
    description='A tiny web application to display and evaluate single-page questionnaires',
    author='Jochen Kupperschmidt',
    author_email='homework@nwsnet.de',
    url='http://homework.nwsnet.de/releases/8909/#el-cuestionario',
    packages=['elcuestionario'],
    install_requires=['flask>=0.10.1'],
    tests_require=['nose2'],
    test_suite='nose2.collector.collector',
)
