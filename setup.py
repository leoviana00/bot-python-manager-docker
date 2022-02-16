# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='bot-python-manager-docker',
    version='0.1.0',
    description='Sample package for manager docker',
    long_description=readme,
    author='Leonardo Viana',
    author_email='leonardoviana00@hotmail.com',
    url='https://github.com/leoviana00/bot-python-manager-docker',
    license=license,
    packages=find_packages()
)