from api_client import get_client, Client
import base64
from proto.profile_pb2 import Profile
import util
from pprint import pprint


async def scrape(credentials: dict) -> dict:
    client = await get_client(credentials)
    encoded_profile_str = await client.get_user('me')
    pprint(util.decode_user_profile(encoded_profile_str), indent=4)
