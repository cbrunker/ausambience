# third party imports
import aiohttp

# project imports
from config import settings


async def async_fetch(url: str, params: dict) -> dict:
    """
    Asynchronous HTTP GET request.

    :param url: Target URL
    :param params: Query parameters
    :return: JSON response as a dictionary
    """
    # ClientSession with timeout handling for quick(er) failover of non-responsive services
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=settings.WEATHER_SERVICE_TIMEOUT)) as session:
        async with session.get(url, params=params) as response:
            return await response.json()

