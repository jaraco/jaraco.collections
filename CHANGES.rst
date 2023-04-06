v4.1.0
======

``Projection`` now accepts an iterable or callable or pattern
for matching keys.

``Projection`` now retains order of keys from the underlying
mapping.

``DictFilter`` is now deprecated in favor of ``Projection``.

v4.0.0
======

``DictFilter`` no longer accepts ``include_keys`` and requires
``include_pattern`` as a keyword argument.

v3.11.0
=======

In ``DictFilter``, deprecated ``include_keys`` parameter and usage
without ``include_pattern``. Future versions will honor
``include_pattern`` as a required keyword argument. All other
uses are deprecated. For uses that currently rely on ``include_keys``,
use ``Projection`` instead/in addition. For example, instead of::

    filtered = DictFilter(orig, include_keys=['a'], include_pattern='b+')

Use::

    filtered = DictFilter(Projection(['a'], orig), include_pattern='b+')

v3.10.0
=======

In ``Projection``, harmonize the implementation and optimize using
``set`` instead of ``tuple``.

v3.9.0
======

``DictFilter.__len__`` no longer relies on the iterable. Improves
efficiency and fixes ``RecursionError`` on PyPy (#12).

v3.8.0
======

Made ``DictStack`` mutable.

v3.7.0
======

Added ``RangeMap.left``.

v3.6.0
======

Revised ``DictFilter``:

 - Fixed issue where ``DictFilter.__contains__`` would raise a ``KeyError``.
 - Relies heavily now on ``collections.abc.Mapping`` base class.

v3.5.2
======

Packaging refresh.

Enrolled with Tidelift.

v3.5.1
======

Fixed ``DictStack.__len__`` and addressed recursion error on
PyPy in ``__getitem__``.

v3.5.0
======

``DictStack`` now supports the following Mapping behaviors:

 - ``.items()``
 - casting to a dict
 - ``__contains__`` (i.e. "x in stack")

Require Python 3.7 or later.

v3.4.0
======

Add ``WeightedLookup``.

v3.3.0
======

Add ``FreezableDefaultDict``.

v3.2.0
======

Rely on PEP 420 for namespace package.

v3.1.0
======

Refreshed packaging. Dropped dependency on six.

v3.0.0
======

Require Python 3.6 or later.

2.1
===

Added ``pop_all`` function.

2.0
===

Switch to `pkgutil namespace technique
<https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages>`_
for the ``jaraco`` namespace.

1.6.0
=====

Fix DeprecationWarnings when referencing abstract base
classes from collections module.

1.5.3
=====

Refresh package metadata.

1.5.2
=====

Fixed KeyError in BijectiveMap when a new value matched
an existing key (but not the reverse). Now a ValueError
is raised as intended.

1.5.1
=====

Refresh packaging.

1.5
===

Added a ``Projection`` class providing a much simpler
interface than DictFilter.

1.4.1
=====

#3: Fixed less-than-equal and greater-than-equal comparisons
in ``Least`` and ``Greatest``.

1.4
===

Added ``Least`` and ``Greatest`` classes, instances of
which always compare lesser or greater than all other
objects.

1.3.2
=====

Fixed failure of KeyTransformingDict to transform keys
on calls to ``.get``.

1.3
===

Moved hosting to Github.

1.2.2
=====

Restore Python 2.7 compatibility.

1.2
===

Add InstrumentedDict.

1.1
===

Conditionally require setup requirements.

1.0
===

Initial functionality taken from jaraco.util 10.8.
