#!/usr/bin/python3
# coding: utf-8

import time
import argparse
from math import ceil
from threading import RLock
from itertools import product

from Shadow import Shadow
from Computer import *

defaultOutput = "output"
defaultMaxSizePass = 12
defaultMinSizePass = 6
defaultThread = 2
defaultCharList = "abcdefghijklmnopqrstuvwxyz"
defaultCharList += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
defaultCharList += "0123456789"
defaultCharList += "@_#"

def check_arg():
	parser = argparse.ArgumentParser(description="Déchiffre un fichier via la méthode force brute")
	parser.add_argument("shadow", help="fichier shadow à déchiffrer", type=str)
	parser.add_argument("-o", "--output", help="nom du fichier de sorti", type=str, default=defaultOutput)
	parser.add_argument("-v", help="verbeux", action="store_true")
	parser.add_argument("--min", help="Taille minimale du mot de passe", default=defaultMinSizePass, type=int)
	parser.add_argument("--max", help="Taille maximale du mot de passe", default=defaultMaxSizePass, type=int)
	parser.add_argument("--thread", help="Nombre de thread à utiliser", default=defaultThread, type=int)
	parser.add_argument("-c", help="Caractères possibles du mot de passe", default=defaultCharList, type=str)
	args = parser.parse_args()
	return (args)

def get_shadows(shadowPath):
	with open(shadowPath, "r") as shadowFile:
		print ("Lecture du fichier shadow...")
		for line in shadowFile:
			shadow = Shadow(line)
			if (shadow.is_decryptable()):
				shadows.append(shadow)

def compute_thread(minPass, maxPass, charList, nbThread):
	if (nbThread >= len(charList)):
		nbThread = len(charList)
	threads = []
	step = ceil(len(charList) / nbThread)
	name = 0
	for i in range(0, len(charList), step):
		endPass = i + step if i + step < len(charList) else len(charList)
		threads.append(Computer(name, minPass, maxPass, i, endPass, charList))
		name += 1
	return (threads)

def manage_threads(threads):
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()

def write_to_output(outputName, verbose):
	with open(outputName, "w") as output:
		for line in passwordsFound:
			out = "{}: \"{}\" trouvé en {}s".format(line[0], line[1], str(round(line[2], 4)))
			output.write(out + "\n")
			if (verbose == True):
				print (out)

def main():
	args = check_arg()
	get_shadows(args.shadow)
	threads = compute_thread(args.min, args.max, args.c, args.thread)
	manage_threads(threads)

main()
