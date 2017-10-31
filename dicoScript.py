#!/usr/bin/python3
# coding: utf-8

# @Author: Maxime Cohen <maxime>
# @Date:   2017-Oct-13 10:01
# @Email:  maxime.cohen-pro@outlook.fr
# @Project:
# @Filename: script.py
# @Last modified by:   maxime
# @Last modified time: 2017-Oct-17 17:06

import time
import argparse
import hashlib

defaultOutput = "output"
hashMethod = {
			"1":hashlib.md5,
			"5":hashlib.sha256,
			"6":hashlib.sha512
			}

def parse_arg():
	parser = argparse.ArgumentParser(description="Déchiffre un fichier via la méthode du dico")
	parser.add_argument("shadow", help="fichier shadow à déchiffrer", type=str)
	parser.add_argument("dico", help="fichier dictionnaire", type=str)
	parser.add_argument("-o", "--output", help="nom du fichier de sorti", type=str, default=defaultOutput)
	parser.add_argument("-v", help="verbeux", action="store_true")
	return (parser.parse_args())

def get_shadows(args):
	shadows = {}
	with open(args.shadow, "r") as shadowFile:
		print ("Lecture du fichier shadow...")
		for line in shadowFile:
			data = line.split(':')
			if (len(data) > 1 and data[1] not in ["!!", "!", "*", "x", ""]):
				hashed = data[1].split('$')
				shadows[data[0]] = [elem for elem in hashed if elem != ""]
	return (shadows)

def generate_password(args):
	with open(args.dico, "r") as dicoFile:
		for password in dicoFile:
			password = password.replace('\n', '') #strip()
			if password != "":
				yield password


def decrypt_shadows(args, shadows):
	timeBeg = time.time()
	for password in generate_password(args):
		if (len(shadows) == 0):
			return
		found = []
		for name, shadow in shadows.items():
			passwordHashed = hashMethod[shadow[0]](password.encode("utf-8")).hexdigest()
			if (passwordHashed == shadow[-1]):
				timeEnd = time.time()
				write_to_output(args, name, password, timeEnd - timeBeg)
				found.append(name)
		for name in found:
			del shadows[name]

def write_to_output(args, shadowName, passwordFound, timeDecrypt):
	out = "Nom:{}, Mot de passe:{}, temps de déchiffrage:{}".format(shadowName, passwordFound, round(timeDecrypt, 4))
	if (args.v == True):
		print(out)
	outputFile.write(out + '\n')

def main():
	args = parse_arg()
	shadows = get_shadows(args)
	global outputFile
	outputFile = open(args.output, "w")
	with outputFile:
		decrypt_shadows(args, shadows)
		outputFile.close()

if __name__ == "__main__":
	main()
