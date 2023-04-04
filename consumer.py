import asyncio
from aiokafka import AIOKafkaConsumer
from aiokafka.helpers import create_ssl_context

import json
import base64
from utils.email_sender import ManyEmailsSender
from utils.user_data_getter import UserData
from utils.storage_manager import AsyncFTPStorageManager
from abc import ABC


class ConsumerSender(ABC):
    def __init__(
        self, sender_topic,sender_group_id, 
        sender_bootstrap_servers,
        ftp_host, ftp_port, ftp_user, 
        ftp_password, api_link, 
        consumer_cert_location, consumer_ca_location, 
        consumer_key_location, consumer_cert_password
        ) -> None:
        context = create_ssl_context(
            certfile=consumer_cert_location,
            cafile=consumer_ca_location,
            keyfile=consumer_key_location,
            password=consumer_cert_password,
        )
        self._consumer = AIOKafkaConsumer(
            sender_topic, group_id=sender_group_id,
            bootstrap_servers=sender_bootstrap_servers,
            enable_auto_commit=False,
            auto_offset_reset='earliest',
            security_protocol='SSL',
            ssl_context=context
        )
        self._storage_manager = AsyncFTPStorageManager(
            ftp_host, ftp_port, ftp_user, ftp_password
        )
        self._user_data = UserData(api_link)
    
    
    async def start(self):
        await self._consumer.start()
        await self._storage_manager.start()
    
        await self._start_consumer_loop()
        
    
    async def _start_consumer_loop(self):
        async for msg in self._consumer:
            message_data = self._serialize_message(msg)
            if not message_data:
                await self._consumer.commit()
            
            email_creds = self._user_data.get_email_creds_by_token(
                message_data['sender']['email'], message_data['user_token']
            )
            user = email_creds.pop('user_id')
            email_creds = self._transform_data_from_api(email_creds)
            sender = ManyEmailsSender(**email_creds)
            print(user, 'text_templates', message_data['text_template'])
            text_template = await self._storage_manager.get_user_file(
                user, 'text_templates', message_data['text_template']
            )
            text_template = text_template.decode('utf-8')
            print('html')
            html_template = await self._storage_manager.get_user_file(
                user, 'html_templates', message_data['html_template']
            )
            html_template = html_template.decode('utf-8')
            
            attachments: dict[str, bytes] = {}
            print('attach')
            for attach in message_data['attachments']:
                attachments[attach] = await self._storage_manager.get_user_file(
                    user, 'attachments', attach
                )
            
            sender.send_emails(
                message_data['subject'],
                text_template,
                html_template,
                message_data['receivers'],
                message_data['common_fields'],
                attachments
            )
            print('done')
            await self._consumer.commit()
    
    
    @staticmethod
    def _serialize_message(msg) -> dict | bool:
        try:
            value = msg.value
            json_bytes = base64.b64decode(value)
            json_str = json_bytes.decode("utf-8")
            return json.loads(json_str)
        except:
            print('serealize error')
            return False
    
    
    @staticmethod
    def _transform_data_from_api(data):
        return {
            "email": data["email"],
            "password": data["password"],
            "host": data["email_host"],
            "port": data["email_port"]
        }


