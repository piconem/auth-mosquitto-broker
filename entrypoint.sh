#!/bin/sh
#RAW CREDENTIAL File is loaded and converted onlyt the first time the container is started
#This approach avoid a multiple generation of password files with the consequent invalidation of the 
#previous credentials. (If the mosquitto_passwd command is executed multiple times on the same the password is re-encrypted)

RAW_PASSWDFILE=/mosquitto/config/raw_credentials.txt
TARGET_PASSWDFILE=/mosquitto/config/credentials.txt

echo "Starting Entrypoint Script ..."

if [ ! -f $TARGET_PASSWDFILE ]; then
    echo "Converting password file"
    mosquitto_passwd -U $RAW_PASSWDFILE
    cp $RAW_PASSWDFILE $TARGET_PASSWDFILE
else
    echo "File already available and correctly converted !"
fi

exec "$@"