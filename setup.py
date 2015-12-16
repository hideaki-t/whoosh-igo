#!/usr/bin/env python
# encoding: utf-8

import io
from setuptools import setup


setup(
    name='whoosh-igo',
    version='0.7',
    description='tokenizers for Whoosh designed for Japanese language',
    long_description= io.open('README', encoding='utf-8').read() + "\n\n" + io.open('CHANGES', encoding='utf-8').read(),
    author='Hideaki Takahashi',
    author_email='mymelo@gmail.com',
    url='https://github.com/hideaki-t/whoosh-igo/',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Natural Language :: Japanese',
                 'Operating System :: OS Independent',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Topic :: Scientific/Engineering :: Information Analysis',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Text Processing :: Linguistic',
                 ],
    keywords=['japanese', 'tokenizer',],
    license='Apache License, Version 2.0',
    packages=['whooshjp'],
    )
