import asks
import click
import trio
import json

from bookface_scraper.config import BASE_URL, MAX_TASKS

asks.init('trio')


class Client:
    def __init__(self):
        self._token = None
        self._session = asks.Session(base_location=BASE_URL,
                                     endpoint='/api/',
                                     connections=MAX_TASKS,
                                     persist_cookies=True)

    async def login(self, credentials) -> str:
        """
        Perform login with provided credentials.
        Raise RuntimeError if encountered issues during login.
        """
        click.secho(f'attempting login to {BASE_URL}/api/login', fg='yellow')
        click.secho(f'credentials - {credentials}', fg='yellow')
        done = False
        attempts = 0
        while not done:
            response = await self._session.post(path='login', json=credentials)

            # check http status code:
            status = response.status_code
            if status != 200:
                if status == 500 and attempts < 3:
                    attempts += 1
                    continue
                click.secho(f'login failed with status code: {status}', fg='red')
                raise RuntimeError(f'bad status during login - {status}')

            # check actual response:
            res_json = response.json()
            if res_json['status'] == 'failure':
                click.secho(f'login failed - reason: {res_json["reason"]}', fg='red')
                return None

            token = response.cookies[0].value
            click.secho(f'login successful. token: {token}', fg='green')
            done = True

    async def get_user(self, user_id: str) -> str:
        """
        Get encoded user profile string.
        """
        done = False
        user_profile = None
        attempts = 0
        while not done:
            response = await self._session.get(path=f'user/{user_id}')
            if response.status_code == 500:
                if attempts > 3:
                    await trio.sleep(10)
                    attempts = 0
                else:
                    attempts += 1
                    continue
            user_profile = response.content
            done = True
        return user_profile

    async def get_followers(self, user_id: str, skip=0) -> list:
        """
        Get list of followers for user.
        """
        done = False
        attempts = 0
        followers = set()
        while not done:
            response = await self._session.get(path=f'user/{user_id}/followers',
                                               params={'skip': skip})
            if response.status_code == 500:
                if attempts > 3:
                    await trio.sleep(10)
                    attempts = 0
                else:
                    attempts += 1
                    continue
            res_json = response.json()
            followers |= {f['id'] for f in res_json['followers']}
            if res_json['more']:
                followers |= await self.get_followers(user_id, skip + 10)
            done = True
        return followers


async def get_client(credentials: dict):
    client = Client()
    await client.login(credentials)
    return client
