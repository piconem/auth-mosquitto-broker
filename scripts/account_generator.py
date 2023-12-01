import random
import string
import sys
import argparse

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

argParser = argparse.ArgumentParser()
argParser.add_argument("-f", "--file", help="Username list file")
argParser.add_argument("-a", "--admin", action="store_true", help="Add the admin ACL")

args = argParser.parse_args()

print("Input Parameters: args=%s" % args)

if args.file is None:
	print("Missing FilePath ! Use -f or --file or run -h to read help")
	sys.exit(1)

print("Target UserName File: args.file=%s" % args.file)

targetFileName = args.file
outputFileName = 'mosquitto_accounts.txt'

print("Reading File: {} \n".format(targetFileName))

# Read target file line by line 
emailListFile = open(targetFileName, 'r') 
Lines = emailListFile.readlines() 

# writing to file 
outputAccountFile = open(outputFileName, 'a')  

print("Admin Account added to file ...\n")

#Write Admin Account
if args.admin is not None and args.admin:
	outputAccountFile.write("admin:ayndrhxmpoqjqhqwqe1231\n")

count = 0
# Strips the newline character 
for line in Lines:
    count = count + 1 
    username = line.strip()
    password = get_random_string(16)
    print("Acccount {} -> {}:{}".format(count, username, password))
    outputAccountFile.write("{}:{}\n".format(username, password))

outputAccountFile.close()

print("\nMosquitto Account File Correctly Generated ! -> {} \n".format(outputFileName))
