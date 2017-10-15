#!/usr/bin/python3
# coding: utf8

# @Author: Maxime Cohen <maxime>
# @Date:   2017-Oct-14 16:49
# @Email:  maxime.cohen-pro@outlook.fr
# @Project:
# @Filename: Shadow.py
# @Last modified by:   maxime
# @Last modified time: 2017-Oct-14 23:36

import hashlib

hashMethod = {
			"1":hashlib.md5,
			"5":hashlib.sha256,
			"6":hashlib.sha512
			}

class Shadow:

	def __init__(self, shadowLine):
		self._name = ""
		self._id = ""
		self._salt = ""
		self._hashed = ""
		self._decryptable = self._parse_shadow(shadowLine)

	def _parse_shadow(self, shadowLine):
		shadowData = shadowLine.split(':')
		if (len(shadowData) < 2 or
		shadowData[1] in ["!!", "!", "*", "x", ""]):
			return (False)
		self._name = shadowData[0]
		shadowPass = shadowData[1].split('$')
		self._hashed = shadowPass.pop(-1)
		if (len(shadowPass) > 1):
			self._id = shadowPass[1]
		if (len(shadowPass) > 2):
			self._salt = shadowPass[2]
		return (True)

	def is_decryptable(self):
		return (self._decryptable)

	def crypt_comp_string(self, string):
		crypted = hashMethod[self._id](string.encode('utf-8')).hexdigest()
		if (crypted == self._hashed):
			return (True)
		return (False)

	def get_name(self):
		return (self._name)

	def __str__(self):
		return ("Shadow: (name:{}, id:{}, salt:{}, hashed:{})".format(self._name, self._id, self._salt, self._hashed))
