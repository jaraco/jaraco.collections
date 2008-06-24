#!python
# -*- coding: utf-8 -*-

# $Id$

import re, sets

class NonDataProperty(object):
	"""Much like the property builtin, but only implements __get__,
	making it a non-data property, and can be subsequently reset.
	
	See http://users.rcn.com/python/download/Descriptor.htm for more
	information."""
	
	def __init__(self, fget):
		assert fget is not None, "fget cannot be none"
		# todo, make sure fget is callable
		self.fget = fget
		
	def __get__(self, obj, objtype=None):
		if obj is None:
			return self
		return self.fget(obj)

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
		self.specified_keys = sets.Set(include_keys)
		if include_pattern is not None:
			self.include_pattern = re.compile(include_pattern)
		else:
			# for performance, replace the pattern_keys property
			self.pattern_keys = sets.Set()

	def get_pattern_keys(self):
		#key_matches = lambda k, v: self.include_pattern.match(k)
		keys = filter(self.include_pattern.match, self.dict.keys())
		return sets.Set(keys)
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

	def __cmp__(myself, yourself):
		return cmp(dict(myself), yourself)

# DictMap is much like the built-in function map.  It takes a dictionary
#  and applys a function to the values of that dictionary, returning a
#  new dictionary with the mapped values in the original keys.
def DictMap(function, dictionary):
	"""
	>>> d = DictMap(lambda x:x+1, dict(a=1, b=2))
	>>> d == dict(a=2,b=3)
	True
	"""
	return dict(zip(dictionary.keys(), map(function, dictionary.values())))

