from motor.motor_asyncio import AsyncIOMotorClient
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.environ.get("MONGODB_URL")
# print("MONGODB_URI:", MONGODB_URL)

ca = certifi.where()
client = AsyncIOMotorClient(MONGODB_URL, tlsCAFile=ca)
db = client.your_database_name