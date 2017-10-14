#!/usr/bin/python3
# coding: utf8
# @Author: Maxime Cohen <maxime>
# @Date:   2017-Oct-13 10:01
# @Email:  maxime.cohen-pro@outlook.fr
# @Project: Snake
# @Filename: script.py
# @Last modified by:   maxime
# @Last modified time: 2017-Oct-14 10:35

import argparse

def check_arg():
	parser = argparse.ArgumentParser(description="Déchiffre un fichier via la méthode du dico")
	parser.add_argument("shadow", help="fichier shadow à déchiffrer", type=str)
	parser.add_argument("dico", help="fichier dictionnaire", type=str)
	parser.add_argument("-o", "--output", help="nom du fichier de sorti", type=str, default="output")
	args = parser.parse_args()
	return (args)

def get_dico(dicoPath):
	with open(dicoPath, "r") as dicoFile:
		tempTab = dicoFile.read().split('\n')
		dico = []
		for line in tempTab:
			if line != "":
				dico.append(line)
	dicoFile.close()
	return (dico)

def get_shadow(shadowPath):
	shadow = {}
	with open(shadowPath, "r") as shadowFile:
		tempTab = shadowFile.read().split("\n")
		shadowTab = []
		for line in tempTab:
			if line != "":
				shadowTab.append(line)
		for shadowLine in shadowTab:
			shadowLine = shadowLine.split(':')
			if (shadowLine[1] not in ["!!", "!", "*"]):
				shadowPass = shadowLine[1].split('$')
				tmp = []
				for line in shadowPass:
					if line != "":
						tmp.append(line)
				shadow[shadowLine[0]] = tmp
	shadowFile.close()
	return (shadow)

def main():
	args = check_arg()
	dico = get_dico(args.dico)
	shadow = get_shadow(args.shadow)
	print (shadow)

main()
