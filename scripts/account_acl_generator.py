import random
import string
import sys
import argparse
import os


def is_account_new(targetUsername, targetFileContent):
    if "{}:".format(targetUsername) in targetFileContent:
        return False
    else:
        return True
        
def is_acl_new(targetUsername, targetFileContent):
    if "user {}".format(targetUsername) in targetFileContent:
        return False
    else:
        return True


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def create_new_user(username, password, basicTopic, isAdminAccount, targetUsernameNameFile, targetAclFile):

    # Target File Content
    targetUsernameFileContent = ""
    if os.path.exists(targetUsernameNameFile):
        targetFileContentDescriptor = open(targetUsernameNameFile, 'r')
        targetFileContent = targetFileContentDescriptor.read()
        targetFileContentDescriptor.close()

    # Target File Content
    targetAclFileContent = ""
    if os.path.exists(targetAclFile):
        targetFileContentDescriptor = open(targetAclFile, 'r')
        targetAclFileContent = targetFileContentDescriptor.read()
        targetFileContentDescriptor.close()

    # writing to file 
    appendAccountFile = open(targetUsernameNameFile, 'a')   
    appendAclFile = open(targetAclFile, 'a')  

    if is_account_new(username, targetUsernameFileContent) and is_acl_new(username, targetAclFileContent):

        if password is None or len(password) == 0:
            print("Generating Password ...")
            password = get_random_string(16)
    
        #Write New Account to file
        
        appendAccountFile.write("{}:{}\n".format(username, password))
        print("\nMosquitto Account File Correctly Updated ! -> {} \n".format(targetUsernameNameFile))

        #write Admin ACL lines
        if isAdminAccount is not None and isAdminAccount:
            admin_acl = ["\n#ADMIN ACL USER {}\n".format(username), "user {}\n".format(username), "topic readwrite #\n\n", "##### USER ACL Rules #####\n"]
            appendAclFile.writelines(admin_acl)
        else:
            basicTopic = basicTopic.rstrip('/')
            topic = "{}/{}/#".format(basicTopic, username)
            print("Setting ACL For Acccount {} and Topic {}".format(username, topic))
            appendAclFile.write("\n#ACL For Username {}\n".format(username))
            appendAclFile.write("user {}\n".format(username))
            appendAclFile.write("topic {}\n".format(topic))
        
        print("\nMosquitto ACL File Correctly Updated ! -> {} \n".format(targetAclFile))
    else:
        print("WARNING ! Username {} already available !".format(username))

    appendAccountFile.close()
    appendAclFile.close()



def generate_accounts(inputUsernameFileName, targetFileName):
      
    print("Reading File: {} \n".format(inputUsernameFileName))

    # Read target file line by line 
    usernameListFile = open(inputUsernameFileName, 'r') 
    usernameList = usernameListFile.readlines() 

    # Target File Content
    targetFileContent = ""
    if os.path.exists(targetFileName):
        targetFileContentDescriptor = open(targetFileName, 'r')
        targetFileContent = targetFileContentDescriptor.read()
        targetFileContentDescriptor.close()

    # writing to file 
    targetFile = open(targetFileName, 'a')  

    print("Admin Account added to file ...\n")

    count = 0

    for targetUsername in usernameList:
        
        targetUsername = targetUsername.strip()
        count = count + 1

        if is_account_new(targetUsername, targetFileContent):
             
            username = targetUsername.strip()
            password = get_random_string(16)
            print("Username {} -> {}:{}".format(count, username, password))
            targetFile.write("{}:{}\n".format(username, password))
        else:
            print("WARNING: Username {} -> {} Already Available !".format(count, targetUsername))

    targetFile.close()

    print("\nMosquitto Account File Correctly Generated ! -> {} \n".format(targetFileName))


def generate_acl(inputUsernameFileName, targetFileName, basicTopic):
    
    print("Reading Username list from File: {} \n".format(targetFileName))

    # Read target file line by line 
    usernameListFile = open(inputUsernameFileName, 'r') 
    usernameList = usernameListFile.readlines() 

    # Target File Content
    targetFileContent = ""
    if os.path.exists(targetFileName):
        targetFileContentDescriptor = open(targetFileName, 'r')
        targetFileContent = targetFileContentDescriptor.read()
        targetFileContentDescriptor.close()

    # writing to file 
    outputAccountFile = open(targetFileName, 'a')  

    count = 0

    # Strips the newline character 
    for targetUsername in usernameList:
        
        targetUsername = targetUsername.strip()
        count = count + 1

        if is_acl_new(targetUsername, targetFileContent):
            username = targetUsername.strip()
            basicTopic = basicTopic.rstrip('/')
            topic = "{}/{}/#".format(basicTopic, username)
            print("Username: {}  -> Setting ACL For Account {} and Topic {}".format(count, username, topic))
            outputAccountFile.write("\n#ACL For Username {}\n".format(username))
            outputAccountFile.write("user {}\n".format(username))
            outputAccountFile.write("topic {}\n".format(topic))
        else:
            print("WARNING: Username: {}  -> ACL Already Available !".format(targetUsername))

    outputAccountFile.close()

    print("\nMosquitto ACL File Correctly Generated ! -> {} \n".format(targetFileName))

if __name__ == "__main__":

    accountsOutputFileName = 'mosquitto_accounts.txt'
    aclOutputFileName = 'mosquitto_acl.txt'

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--file", help="Username list file")
    argParser.add_argument("-t", "--topic", help="Basic Topic for Username")
    argParser.add_argument("-a", "--admin", action="store_true", help="Add the admin ACL")
    argParser.add_argument("-u", "--username", help="Target Username")
    argParser.add_argument("-p", "--password", help="Target Password")

    args = argParser.parse_args()

    # Single User Creation
    if args.username is not None:
        if args.admin is not None and args.admin:
            create_new_user(args.username, args.password, "", args.admin, accountsOutputFileName, aclOutputFileName)
        elif args.topic is not None:
            create_new_user(args.username, args.password, args.topic, args.admin, accountsOutputFileName, aclOutputFileName)
        else:
            print("Missing or Wrong Parameters! Run -h to read help")
    # File Based User Creation    
    else:
        
        if args.file is None:
            print("Missing FilePath ! Use -f or --file for the target fileor run -h to read help")
            sys.exit(1)

        if args.topic is None:
            print("Missing Basic Topic ! Use -t or --topic to set the basic topic for accounts or run -h to read help")
            sys.exit(1)

        print("Input UserName File: args.file=%s" % args.file)

        generate_accounts(args.file, accountsOutputFileName)
        generate_acl(args.file, aclOutputFileName, args.topic)

