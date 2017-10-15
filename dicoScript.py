#!/usr/bin/python3
# coding: utf8

# @Author: Maxime Cohen <maxime>
# @Date:   2017-Oct-13 10:01
# @Email:  maxime.cohen-pro@outlook.fr
# @Project:
# @Filename: script.py
# @Last modified by:   maxime
# @Last modified time: 2017-Oct-15 11:28

import time
import argparse
from Shadow import Shadow

defaultOutput = "output"

def check_arg():
	parser = argparse.ArgumentParser(description="Déchiffre un fichier via la méthode du dico")
	parser.add_argument("shadow", help="fichier shadow à déchiffrer", type=str)
	parser.add_argument("dico", help="fichier dictionnaire", type=str)
	parser.add_argument("-o", "--output", help="nom du fichier de sorti", type=str, default=defaultOutput)
	args = parser.parse_args()
	return (args)

def get_shadows(shadowPath):
	shadows = []
	with open(shadowPath, "r") as shadowFile:
		print ("Lecture du fichier shadow...")
		for line in shadowFile:
			shadow = Shadow(line)
			if (shadow.is_decryptable()):
				shadows.append(shadow)
	return (shadows)

def decrypt_shadows(shadows, dicoPath):
	passwordsFound = []
	with open(dicoPath, "r") as dicoFile:
		timeBeg = time.time()
		for password in dicoFile:
			password = password.replace('\n', '')
			if password != "":
				for shadow in shadows:
					if (shadow.crypt_comp_string(password)):
						passwordsFound.append([shadow.get_name(), password, time.time() - timeBeg])
	dicoFile.close()
	return (passwordsFound)

def write_to_output(outputName, passwordsFound):
	with open(outputName, "w") as output:
		for line in passwordsFound:
			output.write(line[0] + ": \"" + line[1] + "\" trouvé en " + str(round(line[2], 4)) + "s\n")

def main():
	args = check_arg()
	shadows = get_shadows(args.shadow)
	passwordsFound = decrypt_shadows(shadows, args.dico)
	print (passwordsFound)
	write_to_output(args.output, passwordsFound)

main()
