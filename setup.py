# -*- coding: utf-8 -*-

import codecs

from setuptools import setup


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='El Cuestionario',
    version='0.4',
    description='A tiny web application to display and evaluate single-page questionnaires',
    long_description=long_description,
    author='Jochen Kupperschmidt',
    author_email='homework@nwsnet.de',
    url='http://homework.nwsnet.de/releases/8909/#el-cuestionario',
    packages=['elcuestionario'],
    install_requires=['flask>=0.10.1'],
    tests_require=['nose2'],
    test_suite='nose2.collector.collector',
)
