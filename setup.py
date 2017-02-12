"""A python utils library

* https://github.com/theno/utlz
* https://pypi.python.org/pypi/utlz
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

this_dir = path.abspath(path.dirname(__file__))

long_description = ''
with open(path.join(this_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='utlz',
    version='0.4.1',
    description='A python utils library',
    long_description=long_description,
    url='https://github.com/theno/utlz',
    author='Theodor Nolte',
    author_email='utlz@theno.eu',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='python development utilities library',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)
