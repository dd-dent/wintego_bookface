import click
from config import BASE_URL
import trio
import asks
from pprint import pprint
asks.init('trio')


class Client:
    def __init__(self):
        self._token = None
        self._session = asks.Session(base_location=BASE_URL,
                                     endpoint='/api/',
                                     connections=20,
                                     persist_cookies=True)

    async def login(self, credentials) -> str:
        """
        Perform login with provided credentials.
        Raise RuntimeError if encountered issues during login.
        """
        click.secho(f'attempting login to {BASE_URL}/api/login', fg='yellow')
        click.secho(f'credentials - {credentials}', fg='yellow')

        response = await self._session.post(path='login', json=credentials)

        # check http status code:
        status = response.status_code
        if status != 200:
            click.secho(f'login failed with status code: {status}', fg='red')
            raise RuntimeError(f'bad status during login - {status}')

        # check actual response:
        res_json = response.json()
        if res_json['status'] == 'failure':
            click.secho(
                f'login failed - reason: {res_json["reason"]}', fg='red')
            return None

        token = response.cookies[0].value
        click.secho(f'login successful. token: {token}', fg='green')

    async def get_user(self, user_id):
        """
        Get encoded user profile string.
        """
        done = False
        user_profile = None
        while not done:
            response = await self._session.get(path=f'user/{user_id}')
            if response.status_code == 500:
                continue
            user_profile = response.content
            done = True
        return user_profile


async def get_client(credentials: dict):
    client = Client()
    await client.login(credentials)
    return client
