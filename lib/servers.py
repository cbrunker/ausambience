#
# Weather Servers functionality
#

import logging

from pydantic import ValidationError
from fastapi import HTTPException

from config import settings
from lib.models import UnifiedWeatherResponse, WeatherstackResponse, OpenWeatherResponse, WeatherStackFailure, \
    OpenWeatherFailure
from lib.utils import async_fetch


async def fetch_weatherstack(location: str = "Melbourne") -> WeatherstackResponse | WeatherStackFailure:
    """
    Fetch weather from Weatherstack

    :param location: Retrieve weather for given location
    """
    # build query
    params = {"access_key": settings.WEATHERSTACK_API_KEY,
              "query": location}

    # fetch data
    data = await async_fetch(settings.WEATHERSTACK_BASE_URL, params)

    try:
        # build model of returned data
        response = WeatherstackResponse(**data)
    except ValidationError:
        # build model of failed response data
        response = WeatherStackFailure(code=data['error']['code'], info=data['error']['info'])

    return response


async def fetch_openweather(location: str = "Melbourne") -> OpenWeatherResponse | OpenWeatherFailure:
    """
    Fetch weather from OpenWeatherMap

    :param location: Retrieve weather for given location
    """
    params = {"q": location,
              "appid": settings.OPENWEATHER_API_KEY,
              "units": "metric"}

    data = await async_fetch(settings.OPENWEATHER_BASE_URL, params)

    try:
        response = OpenWeatherResponse(**data)
    except ValidationError:
        response = OpenWeatherFailure(**data)

    return response


class WeatherServers:
    """
    WeatherServers class abstracts weather service calls and returns UnifiedWeatherResponse model
    """

    def __init__(self):
        """
        WeatherServers constructor
        """
        # dict objects are ordered, weatherstack has priority by default
        service_map = {'weatherstack': fetch_weatherstack,
                       'openweather': fetch_openweather}

        # clean config entries
        config_entries = [s.strip().lower() for s in settings.WEATHER_SERVICE_PRIORITY.split(',')]
        # obtain valid config entries and map to async service functions
        config_priority = [service_map[s] for s in config_entries if s in service_map]

        if config_priority:
            # where priority has been set, utilise the set priority
            self.services = config_priority
        else:
            # no valid priority found
            self.services = [v for v in service_map.values()]

    async def get_weather(self, city: str) -> UnifiedWeatherResponse:
        """
        Return the weather for a given city

        :param city: city to return weather information for
        :return: response model with wind speed, temp and cache information
        """
        weather_response = None
        for service in self.services:
            try:
                response = await service(city)
                weather_response = UnifiedWeatherResponse(wind_speed=response.wind_speed,
                                                          temperature_degrees=response.temperature_degrees,
                                                          cached=False)
            except AttributeError:
                # Service error received, unable to build weather response model
                logging.warning(f"Service: {response.name}. Code: {response.status_code}. Message: {response.detail}'")
                weather_response = response
            except TimeoutError:
                pass

        if not isinstance(weather_response, UnifiedWeatherResponse):
            # no valid responses provided, raise the last received error
            raise HTTPException(status_code=response.status_code, detail=response.detail)

        return weather_response
