
from aioftp import Client
from abc import ABC, abstractmethod
from ftplib import FTP
import io
import asyncio
class AsyncBaseStorageManager(ABC):
    
    @abstractmethod
    async def start(self): ...
    
    @abstractmethod
    async def get_user_file(self, user, file_type, file_name): ...
    
    @abstractmethod
    async def put_user_file(self, user, file_type, file_name, file_binary): ...
    
    @abstractmethod
    async def delete_user_file(self, user, file_type, file_name): ...

    @staticmethod
    def _calculate_path(*args):
        return '/'.join(args)


class AsyncFTPStorageManager(Client, AsyncBaseStorageManager):
    def __init__(
        self, host, port, 
        user, password, 
        *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
    
    
    async def start(self):
        await self.connect(self.__host, self.__port)
        await self.login(self.__user, self.__password)

    
    async def get_file_list(self, user, file_type):
        path = self._calculate_path(user, file_type)
        path_data = await self.list(path)
        path_list = self.__serialize_path_data_files_list(path_data)
        return path_list
    
    
    @staticmethod
    def __serialize_path_data_files_list(path_data):
        return list(map(lambda x: x[0].parts[-1], path_data))
    
    
    async def get_user_file(self, user, file_type, file_name) -> bytes:
        path = self._calculate_path(user, file_type, file_name)
        print(path)
        downloader = await self.download_stream(path)
        file_binary = await downloader.read()
        await downloader.finish()
        return file_binary
    
    
    async def put_user_file(self, user, file_type, file_name, file_binary):
        await self.make_directory(self._calculate_path(user, file_type))
        path = self._calculate_path(user, file_type, file_name)
        uploader = await self.upload_stream(path)
        await uploader.write(file_binary)
        await uploader.finish()
    
    
    async def delete_user_file(self, user, file_type, file_name):
        path = self._calculate_path(user, file_type, file_name)
        await self.remove(path)
        


class BaseStorageManager(ABC):
    
    @abstractmethod
    async def start(self): ...
    
    @abstractmethod
    def get_user_file(self, user, file_type, file_name): ...
    
    @abstractmethod
    def put_user_file(self, user, file_type, file_name, file_binary): ...
    
    @abstractmethod
    def delete_user_file(self, user, file_type, file_name): ...
    
    @staticmethod
    def _calculate_path(*args):
        return '/'.join(args)
    
    
class FTPStorageManager(FTP, BaseStorageManager):
    def __init__(self, host, port, user, password, *args, **kwargs) -> None:
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        super().__init__(*args, **kwargs)
    
    
    def start(self):
        self.connect(self.__host, self.__port)
        self.login(self.__user, self.__password)
    
    
    def get_file_list(self, user, file_type):
        path = self._calculate_path(user, file_type)
        data = self.nlst(path)
        outp_data = []
        for record in data:
            outp_data.append(record.split('/')[-1])
        return outp_data

    def delete_user_file(self): ...
    def get_user_file(self): ...
    
    def put_user_file(self, user, file_type, file_name, file_binary):
        path = self._calculate_path(user, file_type, file_name)
        file_binary = io.BytesIO(file_binary)
        self.storbinary(f'STOR {path}', file_binary)
        
        