# Mosquitto Broker with Authentication, ACL rules & Python Management Scripts

MQTT broker Continer based on the Eclipse Mosquitto original Docker container (https://hub.docker.com/_/eclipse-mosquitto).
The file mosquistto.conf contains the startup configuration of the broker enabling credentials.txt and acl.txt files as reference for the list of authenticated user and authorized topics.

Folder scripts contains a Python script denoted `account_generator.py` to handle account creation in the following configuration: 

- Username, Password and Basic Topic for the ACL
- Username, Randomly Generate Password and Basic Topic for the ACL
- Admin Account with Username, Password and Basic Topic for the ACL
- Admin Account with Username, Randomly Generate Password and Basic Topic for the ACL
- List of Account from Username List read from a file with randomly generated password and a basic topic

Log and Storage are managed on external container volumes as specified in the start.sh script available in the main project folder.

DISCLAIMER: THIS REPOSITORY IS JUST FOR DEVELOPMENT PURPOSES ! IMPROVEMENT AND BETTER MANAGEMENT CAN BE INTRODUCED :) 

# Build Steps

## Step 1 - Generate the User list and ACL Mosquitto files 

Move into the script directory:

```bash
cd scripts
```

You can create account with the following configurations:

### Create Admin Account & ACL

Create Admin account with password

```bash
python account_acl_generator.py -u admin -p admin -a
```

Create Admin account with password randomly generated

```bash
python account_acl_generator.py -u admin_2 -a
```

Create Admin account with password randomly generated

### Create Account & ACL

Each account will have: 

- username 
- password (randomly generated if generating account from a list of username)
- basic topic used for the ACL (e.g., test_basic_topic). After that topic the account will be free to generate any sub topics (e.g., test_basic_topic/telemetry)

The creation of duplicated account will be avoided by checking previously created account and acls

Create Account with username and password

```bash
python account_acl_generator.py -u test_username -p test_password -t basic_topics
```

Create Account account with password randomly generated

```bash
python account_acl_generator.py -u test_username_2 -t basic_topics
```

Create a list of accounts from a list of username in a target file and randomly generated passwords

```bash
python account_acl_generator.py -f my_username_file.txt -t basic_topics 
```

## Step 2 - Build the Container 

Build the container through the dedicated build.sh script

```bash
./build.sh
```

## Step 3 - Start & Stop the container 

start.sh and stop.sh scripts can be user to run and remote the container.

```bash
./start.sh
```

```bash
./stop.sh
```

MQTT Broker logs are redirected to the file log/mosquitto.log and can be monitored through the following command: 

```bash
tail -f log/mosquitto.log
```

# Linux Permission File Issue 

In order to allow a proper user file management for external volumes use the following command: 

```bash
sudo chown -R 1883:1883 data/
sudo chown -R 1883:1883 log/
```

# Test Server 

```bash
nc -zv 192.168.1.32 7883
```

# Update Container with new Credentials & ACL

Stop, Rebuild the container with new credentials and acl and restart it

```bash
sudo ./update.sh
```

# (IF REQUIRED) Example LogRotate Information 

Create a new logrotate configuration file

```bash
sudo nano /etc/logrotate.d/auth-mosquitto
```

Add the following content:

```bash
../auth-mosquitto-broker/log/mosquitto.log {
    daily
    missingok
    rotate 14
    compress
    notifempty
    sharedscripts
    postrotate
        docker restart auth-mosquitto-broker
    endscript
}
```

Test the configuration: 

```bash
sudo logrotate /etc/logrotate.conf --debug
```

# IMPORTANTE NOTES

- The 'port' option is now deprecated and will be removed in a future version. Please use 'listener' instead.
