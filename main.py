import asyncio
from consumer import ConsumerSender
from utils.env_variables import (
    FTP_HOST, FTP_PASSWORD, FTP_PORT, FTP_USER, API_LINK,
    KAFKA_TOPIC, KAFKA_GROUP_ID, KAFKA_BOOTSTRAP_SERVERS,
    CONSUMER_CERT_LOCATION, CONSUMER_CA_LOCATION, 
    CONSUMER_KEY_LOCATION, CONSUMER_CERT_PASSWORD
)



async def main():
    consumer_sender = ConsumerSender(
        KAFKA_TOPIC, KAFKA_GROUP_ID, KAFKA_BOOTSTRAP_SERVERS,
        FTP_HOST, FTP_PORT, FTP_USER, FTP_PASSWORD, API_LINK,
        CONSUMER_CERT_LOCATION, CONSUMER_CA_LOCATION, 
        CONSUMER_KEY_LOCATION, CONSUMER_CERT_PASSWORD
    )
    await consumer_sender.start()

if __name__ == '__main__':
    asyncio.run(main())





