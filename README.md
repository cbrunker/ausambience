# AusAmbience Weather Service

A scalable and reliable weather reporting service using the asynchronous FastAPI REST framework. 
The service fetches weather information for cities and uses Redis for caching results to reduce external API calls 
and improve response times.

## Features

- Fetches weather data using Weatherstack (primary) and OpenWeatherMap (secondary).
- Failover mechanism: If one primary provider fails, the service automatically uses the other.
- Cached results with TTL to prevent frequent API hits.
- Cache timestamps indicate when the result was last cached.
- Asynchronous architecture for improved performance.
- Scalable, built with cloud deployments (like AWS Lambda) in mind.
- Optionally disable weather providers.
- Weather provider priority configuration.
- Weather provider timeout configuration.

## Requirements

- [Python 3.11](https://www.python.org/downloads/)
  - Programming language utilised 
- [Poetry](https://python-poetry.org/docs/)
  - Used for virtual environment and third party package handling
- [Redis server](https://redis.io/download/)
  - Key/Value cache

Weather services will require registration, visit and register at the following locations:

* [WeatherStack](https://weatherstack.com/product)
* [OpenWeatherMap](https://openweathermap.org/api)

## Environment

Development and testing was conducted on Ubuntu 22.04.2 LTS

## Installation

1. Clone this repository:

```bash
git clone https://github.com/cbrunker/ausambiance.git
cd ausambiance
```

2. Install dependencies using Poetry:

```bash
poetry install
```

3. Set environment variables:

You'll need to set environment variables or use a `.env` file for your API keys and other settings:

```env
WEATHERSTACK_API_KEY=your_key_here
OPENWEATHERMAP_API_KEY=your_key_here
REDIS_URL=redis://localhost:6379/0
```

**Required Environment Variables**

* `WEATHERSTACK_API_KEY`: The WeatherStack registered account's API Key
* `OPENWEATHER_API_KEY`: The OpenWeatherMap registered account's API Key

**Optional Environment Variables**

* `OPENWEATHER_BASE_URL`: URL for OpenWeatherMap
  * Default: `https://api.openweathermap.org/data/2.5/weather`
* `WEATHERSTACK_BASE_URL`:URL for WeatherStack
  * Default: `http://api.weatherstack.com/current`
  * **NOTE**: Depending on your subscription, `https` may not be available
* `REDIS_URL`: protocol and URL for redis connection, **rediss** (TLS) is the recommended connection protocol
  * Default: `redis://localhost:6379/0`
* `REDIS_TTL`: number of seconds to cache result data
  * Default: `3`
* `WEATHER_SERVICE_TIMEOUT`: (Optional) Number of seconds to wait for weather service response
  * Default: `3` 
* `WEATHER_SERVICE_PRIORITY`: (Optional) Comma delimited list of services in order of priority. If a provider is not listed, it will be disabled from use
  * Default: `OpenWeather, WeatherStack`

## Running the Service

Activate the poetry environment:

```bash
poetry shell
```

Run the service:

```bash
uvicorn main:app
```

## Documentation

Visit `http://localhost:8080/docs` for the interactive Swagger API documentation.

Alternatively, visit `http://localhost:8080/redoc` for the interactive ReDoc documentation interface.


## Usage

To fetch weather data for a city:

```bash
curl http://localhost:8080/v1/weather?city=melbourne
```

Response:

```json
{
  "wind_speed": 20.3,
  "temperature_degrees": 29.1,
  "cached": true,
  "cached_time": "2023-08-28T12:34:56.789123"
}
```

## Testing

Testing has been created to be Integration based, avoiding mock API testing and ensuring operational status.

The `BASE_URL` environment variable can be set, targeting a remote (or local) deployment of AusAmbience. By default, 
the local host `http://127.0.0.1:8000` will be utilised.

If running the test locally, ensure the API service is running.

Run tests by changing directory to the `tests` directory, and executing the command:

```bash
poetry run pytest
```

## License

[GNU General Public License v3 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.html)

---
