#!python
# -*- coding: utf-8 -*-

# $Id$


class DictFilter(object):
	"""
	Takes a dict, and simulates a sub-dict based on the keys.
	
	>>> sample = {'a': 1, 'b': 2, 'c': 3}
	>>> filtered = DictFilter(sample, ['a', 'c'])
	>>> filtered == {'a': 1, 'c': 3}
	True
	"""
	def __init__(self, dict, include_keys):
		self.dict = dict
		self.include_keys = set(include_keys)

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

	def __cmp__(myself, yourself):
		return cmp(dict(myself), yourself)