import motor.motor_asyncio
import bcrypt


class Database:
    def __init__(self):
        client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self.users = client['test_database']['users']

    async def user_exists(self, username):
        return self.users.find_one({'username': username})

    async def check_user_password(self, username, password):
        try:
            user_data = await self.users.find_one({'username': username})
            password_hash = user_data['password']
            if bcrypt.checkpw(password.encode('ascii'), password_hash):            
                return True
            else:
                return False
        except Exception:
            return False

    async def register(self, username, password):
        if await self.users.find_one({'username': username}):
            return False

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('ascii'), salt)

        await self.users.insert_one({
            'username': username,
            'password': password_hash
        })
        return True
