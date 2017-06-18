# utlz

A Python utils library

[![Build Status](https://travis-ci.org/theno/utlz.svg?branch=master)](https://travis-ci.org/theno/utlz)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/utlz.svg)](https://pypi.python.org/pypi/utlz)
[![PyPI Version](https://img.shields.io/pypi/v/utlz.svg)](https://pypi.python.org/pypi/utlz)

## Installation

Install the latest version of the pypi python package
[utlz](https://pypi.python.org/pypi/utlz):

```shell
pip install utlz
```

## Development

Clone the source code [repository](https://github.com/theno/utlz):

```bash
git clone https://github.com/theno/utlz.git
cd utlz
```

### Fabfile

The `fabfile.py` contains devel-tasks to be executed with
[Fabric](http://www.fabfile.org/) (maybe you need to
[install](http://www.fabfile.org/installing.html) it):

```
> fab -l

Available commands:

    clean    Delete temporary files not under version control.
    pypi     Build package and upload to pypi.
    pythons  Install latest pythons with pyenv.
    test     Run unit tests.
    tox      Run tox.

# Show task details, e.g. for task `test`:
> fab -d test

Run unit tests.

    Keyword-Args:
        args: Optional arguments passed to pytest
        py: python version to run the tests against

    Example:

        fab test:args=-s,py=py27
```

At first, set up python versions with [pyenv](https://github.com/pyenv/pyenv)
and virtualenvs for development with
[tox](https://tox.readthedocs.io/en/latest/):
```
fab pythons
fab tox
```
Tox creates virtualenvs of different Python versions (if they not exist
already) and runs the unit tests against each virtualenv.

On Ubuntu 16.04 you must install `libpython-dev` and `libpython3-dev` in order
to make the tests passing for Python-2.7 and Python-3.5:

```bash
sudo apt-get install  libpython-dev  libpython3-dev

# Then, rebuild the non-working Python-2.7 and Python-3.5 virtualenv and
# run the unit tests:
fab tox:'-e py27 -e py35 --recreate'
```

### Devel-Commands

Run unit tests against several pythons with tox (needs pythons defined
in envlist of `tox.ini` to be installed with pyenv):

```bash
python3.6 -m tox

# only against one python version:
python3.6 -m tox -e py27

# rebuild virtual environments:
python3.6 -m tox -r
```

Run unit tests with pytest (uses tox virtualenv, replace `py36` by e.g.
`py27` where applicable):

```bash
PYTHONPATH='.' .tox/py36/bin/python -m pytest

# show output
PYTHONPATH='.' .tox/py36/bin/python -m pytest -s
```
