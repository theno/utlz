# utlz

A Python utils library

## Installation

Install latest version of `utlz` from pypi (https://pypi.python.org/pypi/utlz):
```shell
pip install utlz
```

## Development

Clone the source code [repository](https://github.com/theno/utlz):

```bash
git clone https://github.com/theno/utlz.git
```

Run unit tests with pytest

```bash
pip install --user  pytest
PYTHONPATH=".:$PYTHONPATH"  python -m pytest
```

Build package and run tests against several pythons with tox:

```bash
# install tox
pip install tox

# install and activate different python versions
fab setup.pyenv -H localhost
pyenv install  2.6.9  2.7.13  3.3.6  3.4.6  3.5.3  3.6.0
pyenv local  system  2.6.9  2.7.13  3.3.6  3.4.6  3.5.3  3.6.0

# build and run tests
python -m tox
```

Build and publish package:
```bash
# install pypandoc and twine
pip install  pypandoc  twine

# build package
python setup.py sdist

# upload to pypi.org
twine  upload  dist/utlz-<VERSION>.tar.gz


# useful oneliners
rm -rf .tox/; python3.6 -m tox
rm -rf dist/; python3.6 setup.py sdist; ls -hal dist/
python3.6 -m twine  upload  dist/utlz*
```
