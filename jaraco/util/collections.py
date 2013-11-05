
class Everything(object):
	"""
	A collection "containing" every possibly thing.

	>>> 'foo' in Everything()
	True

	>>> import random
	>>> random.randint(1, 999) in Everything()
	True
	"""
	def __contains__(self, other):
		return True
