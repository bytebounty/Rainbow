# -*- coding: utf-8 -*-
import hashlib
import sys
import os
import os.path
from os import path
import glob

##########################################
#Enable ONLY if RAM is fast and abundant.
RAM = False
##########################################

DIR = os.getcwd()

def isFile(path):
	if os.path.isdir(path):
		return False
	elif os.path.isfile(path):
		return True
	else:
		return 3

usage = """
USAGE: """+ sys.argv[0] +""" [HASH TYPE]

OPTIONS:
 SHA1,
 SHA224,
 SHA256,
 SHA384,
 SHA512,
 MD5
"""

if len(sys.argv) < 2:
	print(usage)
	exit()

################

hashType = sys.argv[1].lower()

################

if hashType == "md5":
	def hash(string):
		return hashlib.md5(string.strip()).hexdigest()
elif hashType == "sha1":
	def hash(string):
		return hashlib.sha1(string.strip()).hexdigest()
elif hashType == "sha224":
	def hash(string):
		return hashlib.sha224(string.strip()).hexdigest()
elif hashType == "sha256":
	def hash(string):
		return hashlib.sha256(string.strip()).hexdigest()
elif hashType == "sha384":
	def hash(string):
		return hashlib.sha384(string.strip()).hexdigest()
elif hashType == "sha512":
	def hash(string):
		return hashlib.sha512(string.strip()).hexdigest()
else:
	print(usage)
	exit()


banner = """
▄▄▄   ▄▄▄· ▪    ▐ ▄  ▄▄▄▄·	 ▄▄▌ ▐  ▄▌
▀▄ █·▐█ ▀█ ██  •█▌▐█ ▐█ ▀█▪▪	 ██· █▌▐█
▐▀▀▄ ▄█▀▀█ ▐█· ▐█▐▐▌ ▐█▀▀█▄ ▄█▀▄ ██▪▐█▐▐▌
▐█•█▌▐█ ▪▐▌▐█▌ ██▐█▌ ██▄▪▐█▐█▌.▐▌▐█▌██▐█▌
.▀  ▀ ▀  ▀ ▀▀ ▀▀▀ █▪ ·▀▀▀▀  ▀█▄▀▪ ▀▀▀▀ ▀▪
"""

print(banner)
print("Hash type: " + hashType.upper() + "\n")

while True:
	print(""" [1] Generate rainbow table

 [2] Unhash with rainbow table

 [3] Unhash without rainbow table

 [4] Generate hash based on key
""")
	Input = raw_input("Option: ")
	if Input == "1":
		filename = raw_input("Name of file for rainbow table: ")
		wordlist = raw_input("Path to wordlist file or folder: ")
		print("")
		if isFile(wordlist) == False:
			os.chdir(wordlist)
			wordlist = open(filename, 'a')
			for file in glob.glob("*.txt"):
				if RAM:
					readFile = open(file, 'r')
					readFileLines = readFile.readlines()
				with open(file) as fileobject:
					if RAM == False:
						readFileLines = fileobject
					for line in readFileLines:
						wordlist.writelines(hash(line) + "|" + line)
						if line[0].isalpha():
							line = (line[0].swapcase() + line[1:])
							wordlist.writelines(hash(line) + "|" + line)
			wordlist.close()
		else:
			table = open(filename, 'a')
			if RAM:
				readFile = open(wordlist, 'r')
				readFileLines = readFile.readlines()
			with open(table) as fileobject:
				if RAM == False:
					readFileLines = fileobject
				for line in readFileLines:
					table.writelines(hash(line) + "|" + line)
					if line[0].isalpha():
						line = (line[0].swapcase() + line[1:])
						table.writelines(hash(line) + "|" + line)
			table.close()

	elif Input == "2":
		rainbow = raw_input("Name of file for rainbow table: ")
		if rainbow == "":
			rainbow = "rainbow"
		HASH = raw_input("Hash (or file): ")

		if RAM:
			print("Loading rainbow table...")
			readFile = open(rainbow, 'r')
			readFileLines = readFile.readlines()
			print("Table loaded.\n")

		times = 0

		if isFile(HASH) and path.exists(HASH):
			if RAM:
				print("Loading hashes...")
				readHash = open(HASH, 'r')
				readHashLines = readHash.readlines()
				print("Hashes loaded.\n")
			with open(HASH) as fileobject:
				if RAM == False:
					readHashLines = fileobject
					for line in readHashLines:
						print("Hash: " + line.strip())
						found = False
						with open(rainbow) as fileobject:
							if RAM == False:
								readFileLines = fileobject
							for hashline in readFileLines:
								times += 1
								#print(hashline),
								if line.strip() in hashline:
									if line.strip() == hashline.split("|")[0]:
										found = True
										print("KEY FOUND: " + hashline.split("|")[1])
										break
						if found == False:
							print("[!] KEY NOT FOUND [!]\n")
				print("Compared " + str(times) + " hashes.\n")
		
		else:
			found = False
			with open(rainbow) as fileobject:
				if RAM == False:
					readFileLines = fileobject
				for line in readFileLines:
					times += 1
					#print(line),
					if HASH in line:
						if HASH == line.split("|")[0]:
							found = True
							print("KEY FOUND: " + line.split("|")[1])
							break
			if found == False:
				print("[!] KEY NOT FOUND [!]\n")
			print("Compared " + str(times) + " hashes.\n")
				
				
	elif Input == "3":
		wordlist = raw_input("Path to wordlist file or folder: ")
		HASH = raw_input("Hash (or file): ")
		if RAM:
			print("Loading wordlist...")
			readFile = open(wordlist, 'r')
			readFileLines = readFile.readlines()
			print("Wordlist loaded.\n")
		if isFile(wordlist) == False:
			os.chdir(wordlist)
			for file in glob.glob("*.txt"):
				if RAM:
					readFile = open(file, 'r')
					readFileLines = readFile.readlines()
				with open(file) as fileobject:
					if RAM == False:
						readFileLines = fileobject
					for line in readFileLines:
						if isFile(HASH) and path.exists(HASH):
							found = False
							if RAM:
								print("Loading hashes...")
								hashFile = open(HASH, 'r')
								readHashLines = hashFile.readlines()
								print("Hashes loaded.\n")
							with open(HASH) as fileobject:
								if RAM == False:
									readHashLines = fileobject
								for hashes in readHashLines:
									for line in readFileLines:
										if hash(line) == hashes.strip():
											print("KEY FOUND: " + line)
											found = True
											break
									if found == False:
										print("[!] KEY NOT FOUND [!]\n")
						else:
							found = False
							if hash(line) == HASH:
								print("KEY FOUND: " + line)
								found = True
								break
					if found == False:
						print("[!] KEY NOT FOUND [!]\n")
						break
					else:
						break
		else:
			if RAM:
				readFile = open(wordlist, 'r')
				readFileLines = readFile.readlines()
			with open(wordlist) as fileobject:
				if RAM == False:
					readFileLines = fileobject
				for line in readFileLines:
					if isFile(HASH) and path.exists(HASH):
						found = False
						if RAM:
							print("Loading hashes...")
							hashFile = open(HASH, 'r')
							readHashLines = hashFile.readlines()
							print("Hashes loaded.\n")
						with open(HASH) as fileobject:
							if RAM == False:
								readHashLines = fileobject
							for hashes in readHashLines:
								for line in readFileLines:
									if hash(line) == hashes.strip():
										print("KEY FOUND: " + line)
										found = True
										break
								if found == False:
									print("[!] KEY NOT FOUND [!]\n")
					else:
						found = False
						if hash(line) == HASH:
							print("KEY FOUND: " + line)
							found = True
							break
				if found == False:
					print("[!] KEY NOT FOUND [!]\n")
					break
				else:
					break

	elif Input == "4":
		print("Hash: " + hash( raw_input("Key: ") ) )
		print("")
	else:
		print("\n Invalid option\n")
	if path.exists("tmp"):
		try:
			os.remove("tmp")
		except:
			print("Failed to remove any temporary files.\n")
		os.chdir(DIR)
