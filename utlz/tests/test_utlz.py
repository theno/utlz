import utlz


def test_flo():
    foo = 'AAA'
    bar = 'Bbb'
    baz = 'ccc'

    assert utlz.flo('{foo}.{bar}.{baz}') == 'AAA.Bbb.ccc'

    long_ = '{foo}.{bar}.{baz}'.format(**locals())
    assert utlz.flo('{foo}.{bar}.{baz}') == long_

    very_long = '{foo}.{bar}.{baz}'.format(foo=foo, bar=bar, baz=baz)
    assert utlz.flo('{foo}.{bar}.{baz}') == very_long


def test_flat_list():
    assert utlz.flat_list([[1, 2], [3, 4, 5], [6]]) == [1, 2, 3, 4, 5, 6]


def test_text_with_newlines():
    prefix = 'This is a "very" long string which is longer than 78 chars.  '
    middle = 'Really, it has 79'
    postfx = '.'
    long_text = prefix + middle + postfx
    assert utlz.text_with_newlines(long_text) == prefix + middle + '\n' + postfx
    assert utlz.text_with_newlines(long_text, line_length=79) == long_text
    assert utlz.text_with_newlines(long_text, line_length=80) == long_text
    assert utlz.text_with_newlines(long_text, line_length=900) == long_text
    assert utlz.text_with_newlines(long_text, line_length=0) == long_text
    special_newline = prefix + middle + '\r\n' + postfx
    assert utlz.text_with_newlines(long_text, newline='\r\n') == special_newline


def test_func_has_arg():

    def func1(foo):
        pass

    class Class1(object):

        def __init__(self, bar):
            pass

    assert utlz.func_has_arg(func=func1, arg='foo') is True
    assert utlz.func_has_arg(func=func1, arg='bar') is False
    assert utlz.func_has_arg(func=Class1.__init__, arg='self') is True
    assert utlz.func_has_arg(func=Class1.__init__, arg='bar') is True
    assert utlz.func_has_arg(func=Class1.__init__, arg='baz') is False
