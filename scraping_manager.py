from api_client import Client

class Manager:
    def __init__(self, client: Client):
        self._client = client
        self._users = {}
        self._pending_users = set()

    async def start(self):
        pass

async def get_manager(credentials: dict) -> Manager:
    client = Client(credentials)
    await client.login()
    return Manager(client)