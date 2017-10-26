#!/usr/bin/python3
# coding: utf-8

import time
import argparse
import hashlib

from itertools import product

defaultOutput = "output"
defaultMaxSizePass = 12
defaultMinSizePass = 6
defaultThread = 2
defaultCharList = "abcdefghijklmnopqrstuvwxyz"
defaultCharList += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
defaultCharList += "0123456789"
defaultCharList += "@_#"
hashMethod = {
			"1":hashlib.md5,
			"5":hashlib.sha256,
			"6":hashlib.sha512
			}

def parse_arg():
	parser = argparse.ArgumentParser(description="Déchiffre un fichier via la méthode force brute")
	parser.add_argument("shadow", help="fichier shadow à déchiffrer", type=str)
	parser.add_argument("-o", "--output", help="nom du fichier de sorti", type=str, default=defaultOutput)
	parser.add_argument("-v", help="verbeux", action="store_true")
	parser.add_argument("--min", help="Taille minimale du mot de passe", default=defaultMinSizePass, type=int)
	parser.add_argument("--max", help="Taille maximale du mot de passe", default=defaultMaxSizePass, type=int)
	parser.add_argument("-c", help="Caractères possibles du mot de passe", default=defaultCharList, type=str)
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

def decrypt_shadows(args, shadows):
	timeBeg = time.time()
	for i in range(args.min, args.max + 1):
		combinations = product(args.c, repeat=i)
		for combination in combinations:
			if (len(shadows) == 0):
				return ()
			password = "".join(combination)
			compare_hashed_password(args, shadows, password, timeBeg)

def compare_hashed_password(args, shadows, password, timeBeg):
	found = []
	for name, shadow in shadows.items():
		passwordHashed = hashMethod[shadow[0]](password.encode("utf-8")).hexdigest()
		if (passwordHashed == shadow[1]):
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
