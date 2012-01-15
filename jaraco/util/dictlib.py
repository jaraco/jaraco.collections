# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import re
import sys
import operator
import collections
import itertools

from jaraco.lang.python import callable
import jaraco.util.string
from jaraco.util.properties import NonDataProperty

class DictFilter(object):
	"""
	Takes a dict, and simulates a sub-dict based on the keys.

	>>> sample = {'a': 1, 'b': 2, 'c': 3}
	>>> filtered = DictFilter(sample, ['a', 'c'])
	>>> filtered == {'a': 1, 'c': 3}
	True

	One can also filter by a regular expression pattern

	>>> sample['d'] = 4
	>>> sample['ef'] = 5

	Here we filter for only single-character keys

	>>> filtered = DictFilter(sample, include_pattern='.$')
	>>> filtered == {'a': 1, 'b': 2, 'c': 3, 'd': 4}
	True

	Also note that DictFilter keeps a reference to the original dict, so
	if you modify the original dict, that could modify the filtered dict.

	>>> del sample['d']
	>>> del sample['a']
	>>> filtered == {'b': 2, 'c': 3}
	True

	"""
	def __init__(self, dict, include_keys=[], include_pattern=None):
		self.dict = dict
		self.specified_keys = set(include_keys)
		if include_pattern is not None:
			self.include_pattern = re.compile(include_pattern)
		else:
			# for performance, replace the pattern_keys property
			self.pattern_keys = set()

	def get_pattern_keys(self):
		#key_matches = lambda k, v: self.include_pattern.match(k)
		keys = filter(self.include_pattern.match, self.dict.keys())
		return set(keys)
	pattern_keys = NonDataProperty(get_pattern_keys)

	@property
	def include_keys(self):
		return self.specified_keys.union(self.pattern_keys)

	def keys(self):
		return self.include_keys.intersection(self.dict.keys())

	def values(self):
		keys = self.keys()
		values = map(self.dict.get, keys)
		return values

	def __getitem__(self, i):
		if not i in self.include_keys:
			return KeyError, i
		return self.dict[i]

	def items(self):
		keys = self.keys()
		values = map(self.dict.get, keys)
		return zip(keys, values)

	def __eq__(self, other):
		return dict(self) == other

	def __ne__(self, other):
		return dict(self) != other

def dict_map(function, dictionary):
	"""
	dict_map is much like the built-in function map.  It takes a dictionary
	and applys a function to the values of that dictionary, returning a
	new dictionary with the mapped values in the original keys.

	>>> d = dict_map(lambda x:x+1, dict(a=1, b=2))
	>>> d == dict(a=2,b=3)
	True
	"""
	return dict((key, function(value)) for key, value in dictionary.items())

class RangeMap(dict):
	"""
	A dictionary-like object that uses the keys as bounds for a range.
	Inclusion of the value for that range is determined by the
	key_match_comparator, which defaults to less-than-or-equal.
	A value is returned for a key if it is the first key that matches in
	the sorted list of keys.

	One may supply keyword parameters to be passed to the sort function used
	to sort keys (i.e. cmp [python 2 only], keys, reverse) as sort_params.

	Let's create a map that maps 1-3 -> 'a', 4-6 -> 'b'
	>>> r = RangeMap({3: 'a', 6: 'b'})  # boy, that was easy
	>>> r[1], r[2], r[3], r[4], r[5], r[6]
	(u'a', u'a', u'a', u'b', u'b', u'b')

	Even float values should work so long as the comparison operator
	supports it.
	>>> r[4.5]
	u'b'

	But you'll notice that the way rangemap is defined, it must be open-ended on one side.
	>>> r[0]
	u'a'
	>>> r[-1]
	u'a'

	One can close the open-end of the RangeMap by using undefined_value
	>>> r = RangeMap({0: RangeMap.undefined_value, 3: 'a', 6: 'b'})
	>>> r[0]
	Traceback (most recent call last):
	  ...
	KeyError: 0

	One can get the first or last elements in the range by using RangeMap.Item
	>>> last_item = RangeMap.Item(-1)
	>>> r[last_item]
	u'b'

	.last_item is a shortcut for Item(-1)
	>>> r[RangeMap.last_item]
	u'b'

	Sometimes it's useful to find the bounds for a RangeMap
	>>> r.bounds()
	(0, 6)

	"""
	def __init__(self, source, sort_params = {}, key_match_comparator = operator.le):
		dict.__init__(self, source)
		self.sort_params = sort_params
		self.match = key_match_comparator

	def __getitem__(self, item):
		sorted_keys = sorted(self.keys(), **self.sort_params)
		if isinstance(item, RangeMap.Item):
			result = self.__getitem__(sorted_keys[item])
		else:
			key = self._find_first_match_(sorted_keys, item)
			result = dict.__getitem__(self, key)
			if result is RangeMap.undefined_value:
				raise KeyError(key)
		return result

	def _find_first_match_(self, keys, item):
		is_match = lambda k: self.match(item, k)
		matches = list(filter(is_match, keys))
		if matches:
			return matches[0]
		raise KeyError(item)

	def bounds(self):
		sorted_keys = sorted(self.keys(), **self.sort_params)
		return (
			sorted_keys[RangeMap.first_item],
			sorted_keys[RangeMap.last_item],
		)

	# some special values for the RangeMap
	undefined_value = type(str('RangeValueUndefined'), (object,), {})()
	class Item(int): pass
	first_item = Item(0)
	last_item = Item(-1)

__identity = lambda x: x

def sorted_items(d, key=__identity, reverse=False):
	"""
	Return the items of the dictionary sorted by the keys

	>>> sample = dict(foo=20, bar=42, baz=10)
	>>> tuple(sorted_items(sample))
	(('bar', 42), ('baz', 10), ('foo', 20))

	>>> reverse_string = lambda s: ''.join(reversed(s))
	>>> tuple(sorted_items(sample, key=reverse_string))
	(('foo', 20), ('bar', 42), ('baz', 10))

	>>> tuple(sorted_items(sample, reverse=True))
	(('foo', 20), ('baz', 10), ('bar', 42))
	"""
	# wrap the key func so it operates on the first element of each item
	pairkey_key = lambda item: key(item[0])
	return sorted(d.items(), key=pairkey_key, reverse=reverse)

class FoldedCaseKeyedDict(dict):
	"""A case-insensitive dictionary (keys are compared as insensitive
	if they are strings).
	>>> d = FoldedCaseKeyedDict()
	>>> d['heLlo'] = 'world'
	>>> d
	{u'heLlo': u'world'}
	>>> d['hello']
	u'world'
	>>> 'hello' in d
	True
	>>> 'HELLO' in d
	True
	>>> FoldedCaseKeyedDict({'heLlo': 'world'})
	{u'heLlo': u'world'}
	>>> d = FoldedCaseKeyedDict({'heLlo': 'world'})
	>>> d['hello']
	u'world'
	>>> d['Hello']
	u'world'
	>>> d
	{u'heLlo': u'world'}
	>>> d = FoldedCaseKeyedDict({'heLlo': 'world', 'Hello': 'world'})
	>>> d
	{u'heLlo': u'world'}
	"""
	def __init__(self, *args, **kargs):
		super(FoldedCaseKeyedDict, self).__init__()
		# build a dictionary using the default constructs
		d = dict(*args, **kargs)
		# build this dictionary using case insensitivity.
		for item in d.items():
			self.__setitem__(*item)

	def __setitem__(self, key, val):
		if isinstance(key, basestring):
			key = jaraco.util.string.FoldedCase(key)
		super(FoldedCaseKeyedDict, self).__setitem__(key, val)

	def __getitem__(self, key):
		if isinstance(key, basestring):
			key = jaraco.util.string.FoldedCase(key)
		return super(FoldedCaseKeyedDict, self).__getitem__(key)

	def __contains__(self, key):
		if isinstance(key, basestring):
			key = jaraco.util.string.FoldedCase(key)
		return super(FoldedCaseKeyedDict, self).__contains__(key)

class DictAdapter(object):
	"""
	Provide a getitem interface for attributes of an object.

	Let's say you want to get at the string.lowercase property in a formatted
	string. It's easy with DictAdapter.

	>>> import string
	>>> "lowercase is %(lowercase)s" % DictAdapter(string)
	u'lowercase is abcdefghijklmnopqrstuvwxyz'
	"""
	def __init__(self, wrapped_ob):
		self.object = wrapped_ob

	def __getitem__(self, name):
		return getattr(self.object, name)

class ItemsAsAttributes(object):
	"""
	Mix-in class to enable a mapping object to provide items as
	attributes.

	>>> C = type(str('C'), (dict, ItemsAsAttributes), dict())
	>>> i = C()
	>>> i['foo'] = 'bar'
	>>> i.foo
	u'bar'

	# natural attribute access takes precedence
	>>> i.foo = 'henry'
	>>> i.foo
	u'henry'

	# but as you might expect, the mapping functionality is preserved.
	>>> i['foo']
	u'bar'

	# A normal attribute error should be raised if an attribute is
	#  requested that doesn't exist.
	>>> i.missing
	Traceback (most recent call last):
	...
	AttributeError: 'C' object has no attribute 'missing'

	It also works on dicts that customize __getitem__
	>>> missing_func = lambda self, key: 'missing item'
	>>> C = type(str('C'), (dict, ItemsAsAttributes), dict(__missing__ = missing_func))
	>>> i = C()
	>>> i.missing
	u'missing item'
	>>> i.foo
	u'missing item'
	"""
	def __getattr__(self, key):
		try:
			return getattr(super(ItemsAsAttributes, self), key)
		except AttributeError as e:
			# attempt to get the value from the mapping (return self[key])
			#  but be careful not to lose the original exception context.
			noval = object()
			def _safe_getitem(cont, key, missing_result):
				try:
					return cont[key]
				except KeyError:
					return missing_result
			result = _safe_getitem(self, key, noval)
			if result is not noval:
				return result
			# raise the original exception, but use the original class
			#  name, not 'super'.
			e.message = e.message.replace('super',
				self.__class__.__name__, 1)
			e.args = (e.message,)
			raise

def invert_map(map):
	"""
	Given a dictionary, return another dictionary with keys and values
	switched. If any of the values resolve to the same key, raises
	a ValueError.

	>>> numbers = dict(a=1, b=2, c=3)
	>>> letters = invert_map(numbers)
	>>> letters[1]
	'a'
	>>> numbers['d'] = 3
	>>> invert_map(numbers)
	Traceback (most recent call last):
	...
	ValueError: Key conflict in inverted mapping
	"""
	res = dict((v,k) for k, v in map.iteritems())
	if not len(res) == len(map):
		raise ValueError('Key conflict in inverted mapping')
	return res


class IdentityOverrideMap(dict):
	"""
	A dictionary that by default maps each key to itself, but otherwise
	acts like a normal dictionary.

	>>> d = IdentityOverrideMap()
	>>> d[42]
	42
	>>> d['speed'] = 'speedo'
	>>> d['speed']
	u'speedo'
	"""
	def __missing__(self, key):
		return key

class DictStack(list, collections.Mapping):
	"""
	A stack of dictionaries that behaves as a view on those dictionaries,
	giving preference to the last.

	>>> stack = DictStack([dict(a=1, c=2), dict(b=2, a=2)])
	>>> stack['a']
	2
	>>> stack['b']
	2
	>>> stack['c']
	2
	>>> stack.push(dict(a=3))
	>>> stack['a']
	3
	>>> stack.keys()
	['a', 'c', 'b']
	>>> d = stack.pop()
	>>> stack['a']
	2
	>>> d = stack.pop()
	>>> stack['a']
	1
	"""
	def keys(self):
		return list(set(itertools.chain.from_iterable(c.keys() for c in self)))
	def __getitem__(self, key):
		for scope in reversed(self):
			if key in scope: return scope[key]
		raise KeyError(key)
	push = list.append
