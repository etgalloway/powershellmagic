"""Setup file for powershellmagic."""

from setuptools import setup
from powershellmagic import __version__

description = 'IPython magic for Windows PowerShell'

with open('README.rst') as file:
    long_description = file.read()

_classifiers = [
    'Environment :: Win32 (MS Windows)',
    'Framework :: IPython',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: System :: Shells',
    ]

setup(
    name='powershellmagic',
    version=__version__,
    py_modules=['powershellmagic'],
    author='Eric Galloway',
    author_email='ericgalloway@gmail.com',
    description=description,
    long_description=long_description,
    url='https://github.com/etgalloway/powershellmagic',
    classifiers=_classifiers,
    zip_safe=False,
    install_requires=['ipython']
    )
