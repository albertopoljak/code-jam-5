import aiohttp
from practical_porcupines.utils import ConfigApi

config_api = ConfigApi()
aiohttp_session = aiohttp.ClientSession()

# API_ENDPOINT = f"{config_api.API_DOMAIN}:{config_api.API_PORT}/api"
API_ENDPOINT = "https://jilk.pw/api/v1.0/publicall"


async def get_difference(time_1, time_2):
    """
    > Sends time_1 and time_2 to flask_api
    - time_1 = Start time (%Y:%m:%d:%T)
    - time_2 = End time (%Y:%m:%d:%T)
    < Returns aiohttp response
    """

    payload = {"times": [time_1, time_2]}

    async with aiohttp_session.get(API_ENDPOINT, data=payload) as resp:
        return await resp.json()
