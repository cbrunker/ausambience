#
# Pydantic response models
#

# stdlib imports
from typing import Optional

# third party imports
from pydantic import BaseModel, Field


class WeatherBase(BaseModel):
    """Base model representing essential weather data"""
    wind_speed: float = Field(...,  # '...' means the field is required
                              description="The speed of the wind in km/h.",
                              example=15.5
    )
    temperature_degrees: float = Field(...,
                                       description="The current temperature in degrees Celsius.",
                                       example=22.4
    )


##########################
# Service Response Models
##########################

class WeatherstackResponse(BaseModel):
    """Model for Weatherstack API response"""
    request: dict
    location: dict
    current: dict

    @property
    def wind_speed(self) -> float:
        """Retrieve wind speed."""
        return self.current["wind_speed"]

    @property
    def temperature_degrees(self) -> float:
        """Retrieve temperature in degrees Celsius"""
        return self.current["temperature"]


class OpenWeatherResponse(BaseModel):
    """Model for OpenWeatherMap API response"""
    coord: dict
    main: dict
    wind: dict

    @property
    def wind_speed(self) -> float:
        """Retrieve wind speed"""
        return self.wind["speed"]

    @property
    def temperature_degrees(self) -> float:
        """Retrieve temperature in degrees Celsius"""
        return self.main["temp"]


##########################
# Service Failure Modules
##########################

class WeatherStackFailure(BaseModel):
    """Model for failure responses from WeatherStack service"""
    code: int
    info: str
    name: str = "weatherstack"

    @property
    def status_code(self) -> int:
        """Status code for failure"""
        # weatherstack does not currently provide detailed response codes
        return 503

    @property
    def detail(self) -> str:
        """Message information on failure"""
        # weatherstack does not currently provide detailed response messages
        return "Weather service currently unavailable"


class OpenWeatherFailure(BaseModel):
    """Model for failure responses from OpenWeatherMap service"""
    cod: str
    message: str
    name: str = "openweather"

    @property
    def status_code(self) -> int:
        """Status code for failure"""
        return int(self.cod)

    @property
    def detail(self) -> str:
        """Message information on failure"""
        return self.message


#################
# Unified Models
#################

class UnifiedWeatherResponse(WeatherBase):
    """Unified response for the request endpoint"""
    cached: bool = Field(
        ...,
        description="Indicates whether the returned data is from the cache or fetched anew.",
        example=True
    )
    cached_time: Optional[str] = Field(
        description="The time when the data was cached in ISO 8601 format. "
                    "Attribute is value is null when cached data is not present.",
        example="2023-08-28T12:34:56.789123",
        default=None
    )

