FROM eclipse-mosquitto:2.0.12

COPY entrypoint.sh /entrypoint.sh
COPY credentials.txt /mosquitto/config/raw_credentials.txt
COPY acl.txt /mosquitto/config/acl.txt

ENTRYPOINT ["sh", "/entrypoint.sh"]
CMD ["/usr/sbin/mosquitto","-c","/mosquitto/config/mosquitto.conf"]
