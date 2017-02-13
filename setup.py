"""A python utils library

* https://github.com/theno/utlz
* https://pypi.python.org/pypi/utlz
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

description = 'A python utils library'
long_description = description
this_dir = path.abspath(path.dirname(__file__))
readme_md = path.join(this_dir, 'README.md')
readme_rst = path.join(this_dir, 'README.rst')
try:
    import pypandoc
    long_description = pypandoc.convert(readme_md, 'rst')
    with open(readme_rst, 'w') as out:
        out.write(long_description)
except(IOError, ImportError, RuntimeError):
    with open(readme_rst, encoding='utf-8') as in_:
        long_description = in_.read()

setup(
    name='utlz',
    version='0.5.2',
    description=description,
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
