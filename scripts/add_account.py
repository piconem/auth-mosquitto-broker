import random
import string
import sys

accountFileName = 'mosquitto_accounts.txt'
aclFileName = 'mosquitto_acl.txt'

def check_existing_username(file_content, username):
    if username in file_content:
        return False
    else:
        return True

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


# Ask for username
username = input("Enter new username: ")
print("Username Specified: " + str(username))
# username = ''.join(e for e in username if e.isalnum())

# writing to file 
appendAclFile = open(aclFileName, 'a')  
appendAccountFile = open(accountFileName, 'a')  
readAccountFile = open(accountFileName)
file_content = readAccountFile.read()

if check_existing_username(file_content, username):
    
    print("Generating Password ...\n")
    password = get_random_string(16)
    
    print("New Password:" + password)
    print("\nAcccount -> {}:{}".format(username, password))
    #Write New Account to file
    
    appendAccountFile.write("{}:{}\n".format(username, password))
    print("\nMosquitto Account File Correctly Updated ! -> {} \n".format(accountFileName))

    topic = "/iot/user/{}/#".format(username)
    print("Setting ACL For Acccount {} and Topic {}".format(username, topic))
    appendAclFile.write("\n#ACL For Username {}\n".format(username))
    appendAclFile.write("user {}\n".format(username))
    appendAclFile.write("topic {}\n".format(topic))
    
    print("\nMosquitto ACL File Correctly Generated ! -> {} \n".format(appendAclFile))

else:
    print("\nError ! Username already existing !")

appendAccountFile.close()
readAccountFile.close()
appendAclFile.close()
