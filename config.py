from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Environment variable settings management

    Setting an environment variable to a given attribute name will override the predefined/default value
    """
    # rediss:// TLS based connection recommended
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"
    WEATHERSTACK_BASE_URL: str = "http://api.weatherstack.com/current"
    WEATHERSTACK_API_KEY: str
    OPENWEATHER_API_KEY: str
    REDIS_SECRET: Optional[str] = None

    # Service timeout in seconds
    WEATHER_SERVICE_TIMEOUT: int = 3
    # Cache TTL
    REDIS_TTL: int = 3

    # Weather service priority
    WEATHER_SERVICE_PRIORITY: str = "WeatherStack, OpenWeather"


settings = Settings()
