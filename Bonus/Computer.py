#!/usr/bin/python3
# coding: utf-8

import time
from threading import Thread, RLock
from itertools import product
from copy import deepcopy

from Shadow import Shadow

shadows = []
lockShadow = RLock()
passwordsFound = []
lockPasswordsFound = RLock()

class Computer(Thread):

	def __init__(self, name, minPass, maxPass, begPass, endPass, charList):
		Thread.__init__(self)
		self._name = name
		self._minPass = minPass
		self._maxPass = maxPass
		self._begPass = begPass
		self._endPass = endPass
		self._charList = charList
		self._shadows = []
		for shadow in shadows:
			self._shadows.append(deepcopy(shadow))

	def run(self):
		timeBeg = time.time()
		for i in range(self._minPass - 1, self._maxPass):
			for char in range(self._begPass, self._endPass):
				combinations = product(self._charList, repeat=i)
				for combination in combinations:
					if (len(shadows) == 0):
						return ()
					password = self._charList[char] + "".join(combination)
					for shadow in self._shadows:
						if (shadow.crypt_comp_string(password)):
							print(shadow.get_name(), password, time.time() - timeBeg)
							self._shadows.remove(shadow)

	def __str__(self):
		return ("thread[{}]: (min:{}, max:{}, beg:{}, end:{})".format(
			self._name,
			self._minPass,
			self._maxPass,
			self._charList[self._begPass],
			self._charList[self._endPass] if self._endPass < len(self._charList) else "(end)"
			))
