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


def test_lazy_val():

    def func1(arg):
        func1.calls += 1
        return arg.attr + arg.attr
    func1.calls = 0

    class TestClass:

        baz = utlz.lazy_val(lambda self: 'baz ' + str(self.attr))

        def __init__(self, arg):
            self.attr = arg

        @utlz.lazy_val
        def double(self):
            return func1(self)

        @utlz.lazy_val
        def bar(self):
            return 'foo ' + str(self.attr)

    inst1 = TestClass(111)
    assert func1.calls == 0
    assert inst1.double == 222
    assert func1.calls == 1
    assert inst1.double == 222
    assert func1.calls == 1, 'func1.calls is still 1'
    assert inst1.bar == 'foo 111'
    assert inst1.baz == 'baz 111'
    inst2 = TestClass(333)
    assert inst2.baz == 'baz 333'


def test_namedtuple():
    SimpleTuple = utlz.namedtuple(
        typename='SimpleTuple',
        field_names='foo, bar, baz'
    )
    st1 = SimpleTuple(1, 2, 3)
    assert st1.foo == 1 and st1.bar == 2 and st1.baz == 3
    assert st1[0] == 1 and st1[1] == 2 and st1[2] == 3
    st2 = SimpleTuple(baz='ccc', bar='bbb', foo='aaa')
    assert st2.foo == 'aaa' and st2.bar == 'bbb' and st2.baz == 'ccc'

    WithDefaults = utlz.namedtuple(
        typename='WithDefaults',
        field_names='foo, bar=222, baz=None, bla="hihi"'
    )
    wd1 = WithDefaults('hoho')
    assert str(wd1) == "WithDefaults(foo='hoho', bar=222, baz=None, bla='hihi')"
    wd2 = WithDefaults(baz=True, foo='111')
    assert wd2.baz is True and wd2[0] == '111'

    WithLazyVals = utlz.namedtuple(
        typename='WithLazyVals',
        field_names='foo, bar=22',
        lazy_vals={
            'foo_upper': lambda self: self.foo.upper(),
            'bar_as_str': lambda self: str(self.bar),
        }
    )
    wlv1 = WithLazyVals('Hello, World!')
    assert wlv1.bar_as_str == '22'
    assert wlv1.foo_upper == 'HELLO, WORLD!'
    wlv2 = WithLazyVals('asdf')
    assert wlv2.foo_upper == 'ASDF'
