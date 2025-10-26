from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://mongo:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["mydb"]
collection = db["items"]