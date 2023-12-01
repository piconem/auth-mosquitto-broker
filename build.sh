#!/bin/bash

echo "Stop Running Mosquitto Container ..."
docker stop auth-mosquitto-broker 
docker rm auth-mosquitto-broker 

FILE=scripts/mosquitto_accounts.txt
if [ -f "$FILE" ]; then
	echo "Copying Credentials file ..."
	cp scripts/mosquitto_accounts.txt credentials.txt 
else 
    echo "Using default Credentials file ..."
fi

FILE=scripts/mosquitto_accounts.txt
if [ -f "$FILE" ]; then
	echo "Copying ACL file ..."
	cp scripts/mosquitto_acl.txt acl.txt 
else 
    echo "Using default Acl file ..."
fi 

echo "Building Container with new files ..."

VERSION=$1
NAME="auth-mosquitto-broker"

if [[ ! "$VERSION" ]];
	then
		echo "Missing parameter VERSION."
		echo " Usage $0 <VERSION>."
		echo "Example: $0 1.0"
		exit 1
fi

echo "Building $NAME version $VERSION"
docker build -t $NAME:$VERSION .