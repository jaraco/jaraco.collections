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
