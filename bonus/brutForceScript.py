#!/usr/bin/python3
# coding: utf-8

import argparse

defaultOutput = "output"
defaultMaxSizePass = 12
defaultMinSizePass = 6
defaultThread = 2
defaultCharList = "abcdefghijklmnopqrstuvwxyz"
defaultCharList += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
defaultCharList += "0123456789"
defaultCharList += ";@_#"
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
	pass

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
