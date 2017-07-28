# Enums taken from
# https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python/1695250#1695250


def SimpleEnum(**enums):
    return type('SimpleEnum', (object,), enums)


def EnumeratedEnum(*sequential_enums, **named_enums):
    enums = dict(zip(sequential_enums, range(len(sequential_enums))),
                 **named_enums)
    return type('EnumeratedEnum', (object,), enums)


def Enum(*sequential_enums, **named_enums):
    enums = dict(zip(sequential_enums, range(len(sequential_enums))),
                 **named_enums)
    reverse = dict((value, key) for key, value in enums.items())
    enums['reverse'] = reverse
    return type('Enum', (object,), enums)
