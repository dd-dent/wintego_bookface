from api_client import get_client, Client
from user import User
from pprint import pprint
import trio
from config import MAX_TASKS
import click


class Scraper:
    def __init__(self, pending_users: set, all_users: dict, client: Client):
        # pending_users is a set of user IDs not yet scraped
        self._pending_users = pending_users
        self._all_users = all_users
        self._current_tasks = 0
        self._client = client

    async def scrape(self) -> dict:
        # this block won't exit as long as the spawned tasks are running,
        async with trio.open_nursery() as nursery:
            with click.progressbar(label='scraping...') as pbar:
                # as long as we have pending users to scrape...
                while len(self._pending_users) > 0:
                    # scrape no more than 10 in parallel:
                    while self._current_tasks > MAX_TASKS:
                        await trio.sleep(.1)
                    # spawn a scraping task with poped user id.
                    nursery.start_soon(self._scrape_user,
                                       self._pending_users.pop(),
                                       pbar)
                    self._current_tasks += 1

    async def _scrape_user(self, user_id: str, pbar):
        user = User(await self._client.get_user(user_id))
        user.followers = await self._client.get_followers(user.user_id)
        self._current_tasks -= 1
        pbar.update()


async def get_users_data(credentials: dict) -> dict:
    # init API client and get own data
    client = await get_client(credentials)
    me = User(await client.get_user('me'))
    me.followers = await client.get_followers(me.user_id)

    # use own followers to kickstart the scraping
    pending_users = me.followers.copy()
    scraper = Scraper(pending_users, {me.user_id: me}, client)
    scraped_data = await scraper.scrape()
