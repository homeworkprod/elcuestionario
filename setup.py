#!/usr/env/bin python

from setuptools import setup


setup(
    name='El Cuestionario',
    version='0.0',
    description='A tiny web application to display and evaluate single-page questionnaires',
    author='Jochen Kupperschmidt',
    author_email='homework@nwsnet.de',
    url='http://homework.nwsnet.de/releases/8909/#el-questionario',
    packages=['elcuestionario'],
    install_requires=[
        'Flask >= 0.10.1',
    ],
)
