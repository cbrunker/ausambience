# third party imports
from fastapi import FastAPI, HTTPException

# project imports
from lib.servers import WeatherServers
from lib.cache import cache_in_redis, fetch_from_redis
from lib.models import UnifiedWeatherResponse


app = FastAPI()


@app.get("/v1/weather", response_model=UnifiedWeatherResponse)
async def get_weather(city: str):
    """
    Retrieve weather data for given city.
    """
    redis_key = f"weather_{city}"
    cached_data = await fetch_from_redis(redis_key)
    if cached_data:
        # return cached response if available
        weather_data = UnifiedWeatherResponse(wind_speed=cached_data["wind_speed"],
                                              temperature_degrees=cached_data["temperature_degrees"],
                                              cached=True,
                                              cached_time=cached_data["cached_time"])
    else:
        # obtain response from weather service
        weather_data = await WeatherServers().get_weather(city)

        if weather_data is None:
            raise HTTPException(status_code=503, detail="Weather services currently unavailable")

        # update cache with weather response data
        await cache_in_redis(redis_key, weather_data.model_dump())

    return weather_data
