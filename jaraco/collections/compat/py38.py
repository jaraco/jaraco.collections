import collections.abc
import sys
import typing

if sys.version_info >= (3, 9):
    MutableMapping = collections.abc.MutableMapping
else:
    MutableMapping = typing.MutableMapping
