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

echo "Re-Building Container with new files ..."

VERSION=0.1
NAME="auth-mosquitto-broker"

echo "Building $NAME version $VERSION"
docker build -t $NAME:$VERSION .

echo "Starting Updated Mosquitto Container ..."

docker run --name=auth-mosquitto-broker  \
    -p 7883:7883 \
    -v ${PWD}/mosquitto.conf:/mosquitto/config/mosquitto.conf \
    -v ${PWD}/data:/mosquitto/data \
    -v ${PWD}/log:/mosquitto/log \
    --restart always \
    -d auth-mosquitto-broker:0.1
