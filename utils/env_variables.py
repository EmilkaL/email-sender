import os

KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
KAFKA_GROUP_ID = os.environ.get('KAFKA_GROUP_ID')
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
FTP_HOST = os.environ.get('FTP_HOST')
FTP_PORT = int(os.environ.get('FTP_PORT'))
FTP_USER = os.environ.get('FTP_USER')
FTP_PASSWORD = os.environ.get('FTP_PASSWORD')
API_LINK = 'http://' + str(os.environ.get('API_LINK'))
CONSUMER_CERT_LOCATION = os.environ.get('CONSUMER_CERT_LOCATION', './certs/client.pem')
CONSUMER_CA_LOCATION = os.environ.get('CONSUMER_CA_LOCATION', './certs/root-ca.pem')
CONSUMER_KEY_LOCATION = os.environ.get('CONSUMER_KEY_LOCATION', './certs/client.key')
CONSUMER_CERT_PASSWORD = os.environ.get('CONSUMER_CERT_PASSWORD', '12345678')



