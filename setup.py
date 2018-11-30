#!/usr/bin/env python3

from setuptools import setup, find_packages, findall

setup(
    name='bookface-scraper',
    version='1.0',
    description='scraper',
    packages=find_packages(),
    install_requires=[
        'click',
        'trio',
        'asks',
        'protobuf'],
    setup_requires=['wheel'],
    entry_points='''
        [console_scripts]
        bookface-scraper=bookface_scraper.cli:cli
    '''
)
