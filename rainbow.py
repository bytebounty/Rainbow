# -*- coding: utf-8 -*-
import hashlib
import os
import os.path
from os import path
import glob

def isFile(path):
	if os.path.isdir(path):
		return False
	elif os.path.isfile(path):
		return True
	else:
		return 3

def hash(string):
	return hashlib.md5(string.strip()).hexdigest()

banner = """
▄▄▄   ▄▄▄· ▪    ▐ ▄  ▄▄▄▄·	 ▄▄▌ ▐  ▄▌
▀▄ █·▐█ ▀█ ██  •█▌▐█ ▐█ ▀█▪▪	 ██· █▌▐█
▐▀▀▄ ▄█▀▀█ ▐█· ▐█▐▐▌ ▐█▀▀█▄ ▄█▀▄ ██▪▐█▐▐▌
▐█•█▌▐█ ▪▐▌▐█▌ ██▐█▌ ██▄▪▐█▐█▌.▐▌▐█▌██▐█▌
.▀  ▀ ▀  ▀ ▀▀ ▀▀▀ █▪ ·▀▀▀▀  ▀█▄▀▪ ▀▀▀▀ ▀▪
"""

print(banner)

while True:
	print(""" [1] Generate rainbow table

 [2] Unhash with rainbow table

 [3] Crack hashes without rainbow table

 [4] Generate hash based on key
""")
	Input = raw_input("Option: ")
	if Input == "1":
		filename = raw_input("Name of file for rainbow table: ")
		wordlist = raw_input("Path to wordlist file or folder: ")
		
		if isFile(wordlist) == False:
			os.chdir(wordlist)
			for file in glob.glob("*.txt"):
				#print(file)
				tmp = open("tmp", 'a')
				readFile = open(file, 'r')
				readFileLines = readFile.readlines()
				for line in readFileLines:
					tmp.writelines(line)
			tmp.close()
			wordlist = "tmp"

		readFile = open(wordlist, 'r')
		readFileLines = readFile.readlines()

		wordlist = open(filename, 'a')
		for line in readFileLines:
			wordlist.writelines(hash(line) + "|" + line)
			line = (line[0].swapcase() + line[1:])
			wordlist.writelines(hash(line) + "|" + line)

		wordlist.close()
		
		if path.exists("tmp"):
			try:
				os.remove("tmp")
			except:
				print("Failed to remove tmp file.")
	elif Input == "2":
		rainbow = raw_input("Name of file for rainbow table: ")
		if rainbow == "":
			rainbow = "rainbow"
		HASH = raw_input("Hash (or file): ")

		print("Loading rainbow table...")
		readFile = open(rainbow, 'r')
		readFileLines = readFile.readlines()
		print("Table loaded.\n")

		if isFile(HASH) and path.exists(HASH):
			print("Loading hashes...")
			readHash = open(HASH, 'r')
			readHashLines = readHash.readlines()
			print("Hashes loaded.\n")
			for line in readHashLines:
				print("Hash: " + line.strip())
				found = False
				for hashline in readFileLines:
					#print(hashline),
					if line.strip() in hashline:
						if line.strip() == hashline.split("|")[0]:
							found = True
							print("KEY FOUND: " + hashline.split("|")[1])
							break
				if found == False:
					print("[!] KEY NOT FOUND [!]\n")
		
		else:
			found = False
			for line in readFileLines:
				#print(line),
				if HASH in line:
					if HASH == line.split("|")[0]:
						found = True
						print("KEY FOUND: " + line.split("|")[1])
						break
			if found == False:
				print("[!] KEY NOT FOUND [!]\n")
				
				
	elif Input == "3":
		wordlist = raw_input("Path to wordlist file or folder: ")
		HASH = raw_input("Hash (or file): ")
		if isFile(wordlist) == False:
			os.chdir(wordlist)
			for file in glob.glob("*.txt"):
				#print(file)
				tmp = open("tmp", 'a')
				readFile = open(file, 'r')
				readFileLines = readFile.readlines()
				for line in readFileLines:
					tmp.writelines(line)
			tmp.close()
			wordlist = "tmp"
		print("Loading wordlist...")
		readFile = open(wordlist, 'r')
		readFileLines = readFile.readlines()
		print("Wordlist loaded.\n")
		
		if isFile(HASH) and path.exists(HASH):
			found = False
			
			print("Loading hashes...")
			hashFile = open(HASH, 'r')
			readHashLines = hashFile.readlines()
			print("Hashes loaded.\n")
			
			for hashes in readHashLines:
				for lines in readFileLines:
					if hash(lines) == hashes.strip():
						print("KEY FOUND: " + lines)
						found = True
						break
				if found == False:
					print("[!] KEY NOT FOUND [!]")
		else:
			found = False
			for lines in readFileLines:
				if hash(lines) == HASH:
					print("KEY FOUND: " + lines)
					found = True
					break
			if found == False:
				print("[!] KEY NOT FOUND [!]")

	elif Input == "4":
		print("Hash: " + hash( raw_input("Key: ") ) )
