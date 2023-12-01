#!/bin/bash

docker run --name=auth-mosquitto-broker  \
    -p 1883:1883 \
    -p 9001:9001 \
    -v ${PWD}/mosquitto.conf:/mosquitto/config/mosquitto.conf \
    -v ${PWD}/data:/mosquitto/data \
    -v ${PWD}/log:/mosquitto/log \
    --restart always \
    -d auth-mosquitto-broker:0.1