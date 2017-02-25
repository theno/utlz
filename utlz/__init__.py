# -*- coding: utf-8 -*-
import collections
import functools
import json
import inspect
import os.path
import shutil
import sys
import struct
import time
from functools import wraps


# inspired by: http://stackoverflow.com/a/6618825
def flo(string):
    '''Return the string given by param formatted with the callers locals.'''
    callers_locals = {}
    frame = inspect.currentframe()
    try:
        outerframe = frame.f_back
        callers_locals = outerframe.f_locals
    finally:
        del frame
    return string.format(**callers_locals)


# does not work if called from another package (with other globals)
# TODO: unit tests
def doc1():
    '''Return the first line of the (callers) docstring.'''
    return globals()[inspect.stack()[1][3]].__doc__.splitlines()[0]


# TODO: unit tests
def _wrap_with(color_code):
    '''Color wrapper.

    Example:
        >>> blue = _wrap_with('34')
        >>> print(blue('text'))
        \033[34mtext\033[0m
    '''
    def inner(text, bold=False):
        '''Inner color function.'''
        code = color_code
        if bold:
            code = flo("1;{code}")
        return flo('\033[{code}m{text}\033[0m')
    return inner


black = _wrap_with('30')
red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')
default_color = _wrap_with('0')


# TODO: unit tests
def first_paragraph(multiline_str, without_trailing_dot=True, maxlength=None):
    '''Return first paragraph of multiline_str as a oneliner.

    When without_trailing_dot is True, the last char of the first paragraph
    will be removed, if it is a dot ('.').

    Examples:
        >>> multiline_str = 'first line\\nsecond line\\n\\nnext paragraph'
        >>> print(first_paragraph(multiline_str))
        first line second line

        >>> multiline_str = 'first \\n second \\n  \\n next paragraph '
        >>> print(first_paragraph(multiline_str))
        first second

        >>> multiline_str = 'first line\\nsecond line\\n\\nnext paragraph'
        >>> print(first_paragraph(multiline_str, maxlength=3))
        fir

        >>> multiline_str = 'first line\\nsecond line\\n\\nnext paragraph'
        >>> print(first_paragraph(multiline_str, maxlength=78))
        first line second line

        >>> multiline_str = 'first line.'
        >>> print(first_paragraph(multiline_str))
        first line

        >>> multiline_str = 'first line.'
        >>> print(first_paragraph(multiline_str, without_trailing_dot=False))
        first line.

        >>> multiline_str = ''
        >>> print(first_paragraph(multiline_str))
        <BLANKLINE>
    '''
    stripped = '\n'.join([line.strip() for line in multiline_str.splitlines()])
    paragraph = stripped.split('\n\n')[0]
    res = paragraph.replace('\n', ' ')
    if without_trailing_dot:
        res = res.rsplit('.', 1)[0]
    if maxlength:
        res = res[0:maxlength]
    return res


# for decorator with arguments see: http://stackoverflow.com/a/5929165
# TODO: unit tests
def print_doc1(*args, **kwargs):
    '''Print the first paragraph of the docstring of the decorated function.

    The paragraph will be printed as a oneliner.

    May be invoked as a simple, argument-less decorator (i.e. ``@print_doc1``)
    or with named arguments ``color``, ``bold``, ``prefix`` of ``tail``
    (eg. ``@print_doc1(color=utils.red, bold=True, prefix=' ')``).

    Examples:
    #    >>> @print_doc1
    #    ... def foo():
    #    ...     """First line of docstring.
    #    ...
    #    ...     another line.
    #    ...     """
    #    ...     pass
    #    ...
    #    >>> foo()
    #    \033[34mFirst line of docstring\033[0m

    #    >>> @print_doc1
    #    ... def foo():
    #    ...     """First paragraph of docstring which contains more than one
    #    ...     line.
    #    ...
    #    ...     Another paragraph.
    #    ...     """
    #    ...     pass
    #    ...
    #    >>> foo()
    #    \033[34mFirst paragraph of docstring which contains more than one line\033[0m
    '''
    # output settings from kwargs or take defaults
    color = kwargs.get('color', blue)
    bold = kwargs.get('bold', False)
    prefix = kwargs.get('prefix', '')
    tail = kwargs.get('tail', '\n')

    def real_decorator(func):
        '''real decorator function'''
        @wraps(func)
        def wrapper(*args, **kwargs):
            '''the wrapper function'''
            try:
                prgf = first_paragraph(func.__doc__)
                print(color(prefix + prgf + tail, bold))
            except AttributeError as exc:
                name = func.__name__
                print(red(flo('{name}() has no docstring')))
                raise(exc)
            return func(*args, **kwargs)
        return wrapper

    invoked = bool(not args or kwargs)
    if not invoked:
        # invoke decorator function which returns the wrapper function
        return real_decorator(func=args[0])

    return real_decorator


# TODO: unit tests
def print_full_name(*args, **kwargs):
    '''Decorator, print the full name of the decorated function.

    May be invoked as a simple, argument-less decorator (i.e. ``@print_doc1``)
    or with named arguments ``color``, ``bold``, or ``prefix``
    (eg. ``@print_doc1(color=utils.red, bold=True, prefix=' ')``).
    '''
    color = kwargs.get('color', default_color)
    bold = kwargs.get('bold', False)
    prefix = kwargs.get('prefix', '')
    tail = kwargs.get('tail', '')

    def real_decorator(func):
        '''real decorator function'''
        @wraps(func)
        def wrapper(*args, **kwargs):
            '''the wrapper function'''
            first_line = ''
            try:
                first_line = func.__module__ + '.' + func.__qualname__
            except AttributeError as exc:
                first_line = func.__name__
            print(color(prefix + first_line + tail, bold))
            return func(*args, **kwargs)
        return wrapper

    invoked = bool(not args or kwargs)
    if not invoked:
        # invoke decorator function which returns the wrapper function
        return real_decorator(func=args[0])

    return real_decorator


# taken from: http://stackoverflow.com/a/3041990
# TODO: unit tests
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
    It must be "yes" (the default), "no", or None (which means an answer
    of the user is required).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, '1': True,
             "no": False, "n": False, '0': False, }
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


# TODO: unit tests
def query_input(question, default=None, color=default_color):
    """Ask a question for input via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.

    The "answer" return value is a str.
    """
    if default is None or default == '':
        prompt = ' '
    elif type(default) == str:
        prompt = flo(' [{default}] ')
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(color(question + prompt))
        choice = raw_input()
        if default is not None and choice == '':
            return default
        if choice != '':
            return choice


# TODO: unit tests
def filled_out_template_str(template, **substitutions):
    '''Return str template with applied substitutions.

    Example:
        >>> template = 'Asyl for {{name}} {{surname}}!'
        >>> filled_out_template_str(template, name='Edward', surname='Snowden')
        'Asyl for Edward Snowden!'

        >>> template = '[[[foo]]] was substituted by {{foo}}'
        >>> filled_out_template_str(template, foo='bar')
        '{{foo}} was substituted by bar'

        >>> template = 'names wrapped by {single} {curly} {braces} {{curly}}'
        >>> filled_out_template_str(template, curly='remains unchanged')
        'names wrapped by {single} {curly} {braces} remains unchanged'
    '''
    template = template.replace('{', '{{')
    template = template.replace('}', '}}')
    template = template.replace('{{{{', '{')
    template = template.replace('}}}}', '}')
    template = template.format(**substitutions)
    template = template.replace('{{', '{')
    template = template.replace('}}', '}')
    template = template.replace('[[[', '{{')
    template = template.replace(']]]', '}}')
    return template


# TODO: unit tests
def filled_out_template(filename, **substitutions):
    '''Return content of file filename with applied substitutions.'''
    res = None
    with open(filename, 'r') as fp:
        template = fp.read()
        res = filled_out_template_str(template, **substitutions)
    return res


# cf. http://stackoverflow.com/a/126389
# TODO: unit tests
def update_or_append_line(filename, prefix, new_line, keep_backup=True,
                          append=True):
    '''Search in file 'filename' for a line starting with 'prefix' and replace
    the line by 'new_line'.

    If a line starting with 'prefix' not exists 'new_line' will be appended.
    If the file not exists, it will be created.

    Return False if new_line was appended, else True (i.e. if the prefix was
    found within of the file).
    '''
    same_line_exists, line_updated = False, False
    filename = os.path.expanduser(filename)
    if os.path.isfile(filename):
        backup = filename + '~'
        shutil.move(filename, backup)
    #    with open(filename, 'w') as dest, open(backup, 'r') as source:
        with open(filename, 'w') as dest:
            with open(backup, 'r') as source:
                # try update..
                for line in source:
                    if line == new_line:
                        same_line_exists = True
                    if line.startswith(prefix):
                        dest.write(new_line + '\n')
                        line_updated = True
                    else:
                        dest.write(line)
                # ..or append
                if not (same_line_exists or line_updated) and append:
                    dest.write(new_line + '\n')
        if not keep_backup:
            os.remove(backup)
    else:
        with open(filename, 'w') as dest:
            dest.write(new_line + '\n')
    return same_line_exists or line_updated


# TODO: unit tests
def comment_out_line(filename, line, comment='#',
                     update_or_append_line=update_or_append_line):
    '''Comment line out by putting a comment sign in front of the line.

    If the file does not contain the line, the files content will not be
    changed (but the file will be touched in every case).
    '''
    update_or_append_line(filename, prefix=line, new_line=comment+line,
                          append=False)


# TODO: unit tests
def uncomment_or_update_or_append_line(filename, prefix, new_line, comment='#',
                                       keep_backup=True,
                                       update_or_append_line=update_or_append_line):
    '''Remove the comment of an commented out line and make the line "active".

    If such an commented out line not exists it would be appended.
    '''
    uncommented = update_or_append_line(filename, prefix=comment+prefix,
                                        new_line=new_line,
                                        keep_backup=keep_backup, append=False)
    if not uncommented:
        update_or_append_line(filename, prefix, new_line,
                              keep_backup=keep_backup, append=True)


# idea comes from http://stackoverflow.com/a/13105359
# TODO: unit tests
def convert_unicode_2_utf8(input):
    '''Return a copy of `input` with every str component encoded from unicode to
    utf-8.
    '''
    if isinstance(input, dict):
        try:
            # python-2.6
            return dict((convert_unicode_2_utf8(key), convert_unicode_2_utf8(value))
                        for key, value
                        in input.iteritems())
        except AttributeError:
            # since python-2.7 cf. http://stackoverflow.com/a/1747827
            # [the ugly eval('...') is required for a valid syntax on
            # python-2.6, cf. http://stackoverflow.com/a/25049535]
            return eval('''{convert_unicode_2_utf8(key): convert_unicode_2_utf8(value)
                           for key, value
                           in input.items()}''')
    elif isinstance(input, list):
        return [convert_unicode_2_utf8(element) for element in input]
    # elif order relevant: python2 vs. python3
    # cf. http://stackoverflow.com/a/19877309
    elif isinstance(input, str):
        return input
    else:
        try:
            if eval('''isinstance(input, unicode)'''):
                return input.encode('utf-8')
        except NameError:
            # unicode does not exist in python-3.x
            pass
        return input


def load_json(filename):
    '''Return the json-file data, with all strings utf-8 encoded.'''
    data = None
    with open(filename, 'r') as fh:
        data = json.load(fh)
        data = convert_unicode_2_utf8(data)
    return data


def write_json(data, filename):
    '''Write the python data structure as a json-Object to filename.'''
    with open(filename, 'w') as fh:
        json.dump(obj=data, fp=fh, sort_keys=True)


def flat_list(list_of_lists):
    '''Return a simple list out of a list of lists.'''
    return [item for sublist in list_of_lists for item in sublist]


def text_with_newlines(text, line_length=78, newline='\n'):
    '''Return text with a `newline` inserted after each `line_length` char.

    Return `text` unchanged if line_length == 0.
    '''
    if line_length > 0:
        if len(text) <= line_length:
            return text
        else:
            return text[:line_length] + newline + \
                   text_with_newlines(text[line_length:], line_length, newline)
    else:
        return text


def func_has_arg(func, arg):
    '''Return True if an argument `arg` exists for function `func`, else False.
    '''
    return arg in inspect.getargspec(func).args


# originally written by Giampaolo Rodolà and Ken Seehof
# https://code.activestate.com/recipes/576563-cached-property/#c3
def lazy_val(func, key=lambda *args: args[0]):
    '''A memoize decorator for class properties.

    Return a cached property that is calculated by function `func` on first
    access.
    '''

    @functools.wraps(func)
    def get(self):
        try:
            return self._cache[key(func, self)]
        except AttributeError:
            self._cache = {}
        except KeyError:
            pass
        val = self._cache[key(func, self)] = func(self)
        return val

    return property(get)


# namedtuple with defaults and lazy_vals
def namedtuple(typename, field_names, lazy_vals=None, **kwargs):
    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split()
    field_names = list(map(str, field_names))
    field_names_without_defaults = []
    defaults = []
    for name in field_names:
        list_ = name.split('=', 1)
        if len(list_) > 1:
            name, default = list_
            defaults.append(eval(default))
        elif len(defaults) != 0:
            raise ValueError('non-keyword arg after keyword arg in field_names')
        field_names_without_defaults.append(name)
    _class = collections.namedtuple(typename, field_names_without_defaults,
                                    **kwargs)
    _class.__new__.__defaults__ = tuple(defaults)
    if lazy_vals is not None:
        # namedtuple instances are tuples and so they are immutable.  We cannot
        # add an instance property _cache.  So we create one global _cache dict
        # as a class property for storing the lazy vals and use as a key a
        # combination of the identities of self and the func.
        _class._cache = {}
        for attr_name, func in lazy_vals.items():
            setattr(_class, attr_name,
                    lazy_val(func, key=lambda *args: ''.join([str(id(arg))
                                                              for arg
                                                              in args])))
    return _class


# TODO unit test
class StructContext(object):
    '''An instance of this is a file like object which enables access of an
    (data) struct.
    '''

    def __init__(self, data_struct):
        self.data_struct = data_struct
        self.offset = 0

    def __enter__(self):
        self.seek(0)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.seek(0)

    def seek(self, offset):
        self.offset = offset

    def read(self, fmt):
        data = struct.unpack_from(fmt, self.data_struct, self.offset)
        self.offset += struct.calcsize(fmt)
        if len(data) == 1:
            return data[0]
        return data

    @lazy_val
    def length(self):
        return len(self.data_struct)


# https://stackoverflow.com/a/15190306
# TODO: unit tests
class timeout(object):
    '''timeout context.

    Usage example:
        >>> with timeout(0.1) as t:
        ...   while True:
        ...     if t.timed_out:
        ...       break
        ...     print('.')
        ...     time.sleep(0.02)
        .
        .
        .
        .
        .

    For more usage, see https://stackoverflow.com/a/15190306
    '''

    def __init__(self, seconds):
        self.seconds = seconds

    def __enter__(self):
        self.die_after = time.time() + self.seconds
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def timed_out(self):
        return time.time() > self.die_after


if __name__ == '__main__':
    import doctest
    doctest.testmod()
#    Repo = namedtuple('Repo', "url, name=None, basedir='~/repos'")
    Repo = namedtuple('Repo', "url, name=None, basedir='~/repos'")
    assert Repo.__new__.__defaults__ == (None, '~/repos')
    r = Repo(url='https://github.com/theno/fabsetup.git')
    assert r.__repr__() == 'Repo(' \
                           'url=\'https://github.com/theno/fabsetup.git\', ' \
                           'name=None, basedir=\'~/repos\')'
