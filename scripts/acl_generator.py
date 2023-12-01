import random
import string
import sys
import argparse

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
outputFileName = 'mosquitto_acl.txt'

print("Reading Username list from File: {} \n".format(targetFileName))

# Read target file line by line 
usernameListFile = open(targetFileName, 'r') 
Lines = usernameListFile.readlines() 

# writing to file 
outputAccountFile = open(outputFileName, 'a')  

#write Admin ACL lines
if args.admin is not None and args.admin:
	L = ["#ADMIN ACL\n", "user admin\n", "topic readwrite #\n\n", "##### USER ACL Rules #####\n"]
	outputAccountFile.writelines(L)

# Strips the newline character 
for line in Lines:
    username = line.strip()
    topic = "/iot/user/{}/#".format(username)
    print("Setting ACL For Acccount {} and Topic {}".format(username, topic))
    outputAccountFile.write("\n#ACL For Username {}\n".format(username))
    outputAccountFile.write("user {}\n".format(username))
    outputAccountFile.write("topic {}\n".format(topic))

outputAccountFile.close()

print("\nMosquitto ACL File Correctly Generated ! -> {} \n".format(outputFileName))
