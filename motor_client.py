import motor.motor_asyncio as m_m_a
import os

class SingletonClient:
    client = None
    db = None

    @staticmethod
    async def get_client():
        if SingletonClient.client is None:
            MONGODB_USERNAME = os.environ['MONGODB_USERNAME']
            MONGODB_PASSWORD = os.environ['MONGODB_PASSWORD']
            MONGODB_HOSTNAME = os.environ['MONGODB_HOSTNAME']
            MONGODB_DATABASE = os.environ['MONGODB_DATABASE']
            MONGODB_PORT = os.environ['MONGODB_PORT']
            
            SingletonEngine.client = await m_m_a.AsyncIOMotorClient("mongodb://{}:{}@{}:{}}/{}".format(
                MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_HOSTNAME, MONGODB_PORT, MONGODB_DATABASE))

        return SingletonClient.client

    @staticmethod
    async def get_data_base():
        if SingletonClient.db is None:
            client = await SingletonClient.get_client()
            MONGODB_DATABASE = os.environ['MONGODB_DATABASE']
            db = client[MONGODB_DATABASE]
        
        return db
        
