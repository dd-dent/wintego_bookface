from bookface_scraper.api_client import get_client, Client
from bookface_scraper.user import User
import trio
from bookface_scraper.config import MAX_TASKS
from tqdm import tqdm


class Scraper:
    def __init__(self, pending_users: set, all_users: dict, client: Client):

        self._pending_users = pending_users  # users waiting to be scraped
        self._current_users = set()  # users currently being scraped
        self._all_users = all_users  # scraped users go here
        self._client = client  # API client

    async def scrape(self, limit) -> dict:
        # this block won't exit as long as any spawned tasks are running,
        async with trio.open_nursery() as nursery:
            with tqdm(unit=' users', unit_scale=True, smoothing=0) as pbar:
                # if running with limit, run up to limit:
                if limit:
                    for _ in range(limit):
                        await self._spawn_task(nursery, pbar)
                # else run as long as there are pending users to scrape:
                else:    
                    while len(self._pending_users) > 0:
                        await self._spawn_task(nursery, pbar)
        return self._all_users

    async def _spawn_task(self, nursery, pbar):
        # scrape no more than MAX_TASKS concurrently:
        while len(self._current_users) > MAX_TASKS:
            await trio.sleep(.05)
        # pop user id from pending and add to current:
        current_user_id = self._pending_users.pop()
        self._current_users.add(current_user_id)
        # spawn a scraping task with poped user id.
        nursery.start_soon(self._scrape_user,
                            current_user_id,
                            pbar)

    async def _scrape_user(self, user_id: str, pbar):
        # get new user and followers, add to all_users:
        user = User(await self._client.get_user(user_id))
        user.followers = await self._client.get_followers(user.user_id)
        self._all_users[user.user_id] = user

        # get new pending users by subtracting the new followers we just got
        # from users which are already or are currently being scraped and then
        # combining them with the currently pending users:
        new_user_ids = user.followers - self._all_users.keys() - self._current_users
        self._pending_users = new_user_ids | self._pending_users
        
        # finally, remove the user id from current_users:
        self._current_users.remove(user_id)
        pbar.set_postfix(pending=len(self._pending_users))
        pbar.update()


async def get_users_data(credentials: dict, limit) -> dict:
    # init API client and get own data:
    client = await get_client(credentials)
    me = User(await client.get_user('me'))
    me.followers = await client.get_followers(me.user_id)

    # use own followers to kickstart the scraper:
    pending_users = me.followers.copy()
    scraper = Scraper(pending_users, {me.user_id: me}, client)
    scraped_data = await scraper.scrape(limit)

    # populate the list of followed people for each user
    for user_id in scraped_data.keys():
        for follower in scraped_data[user_id].followers:
            if scraped_data.get(follower) is None:
                continue
            scraped_data[follower].following.add(user_id)
    return scraped_data
