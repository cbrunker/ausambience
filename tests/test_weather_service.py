#
# Integration tests
#

import os
import asyncio
from datetime import datetime

import pytest
import httpx


# BASE_URL environment variable will be utilised if present
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

@pytest.mark.asyncio
async def test_primary_provider_real_request():
    # obtain a weather result for melbourne
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/v1/weather?city=melbourne")
    assert response.status_code == 200

    # Check for presence of keys and appropriate data type
    data = response.json()
    assert 'wind_speed' in data and isinstance(data['wind_speed'], (float, int))
    assert 'temperature_degrees' in data and isinstance(data['temperature_degrees'], (float, int))


@pytest.mark.asyncio
async def test_cache_behavior():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # first request to populate cache - use a different city from other tests to avoid pre-cached data
        first_response = await client.get("/v1/weather?city=adelaide")
        assert first_response.status_code == 200
        first_data = first_response.json()

        # data should not be cached
        assert first_data['cached'] is False
        assert first_data['cached_time'] is None

        # second request should be cached data
        second_response = await client.get("/v1/weather?city=adelaide")
        assert second_response.status_code == 200
        second_data = second_response.json()

    # cached attribute should be True
    assert 'cached' in second_data and second_data['cached'] is True
    # timestamp must be present
    assert 'cached_time' in second_data and isinstance(second_data['cached_time'], str)

    # time format must be ISO 8601
    try:
        datetime.fromisoformat(second_data['cached_time'])
    except ValueError:
        assert False, "cached_time is not in ISO 8601 format"


@pytest.mark.asyncio
async def test_cache_expiry_behavior():
    # ttl of 3 seconds
    ttl = 3
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # use a different city to avoid pre-caching
        first_response = await client.get("/v1/weather?city=perth")
        assert first_response.status_code == 200

        first_data = first_response.json()

        # data should not be cached
        assert first_data['cached'] is False
        assert first_data['cached_time'] is None

        # Wait for TTL to expire, plus 1 second buffer
        await asyncio.sleep(ttl + 1)

        second_response = await client.get("/v1/weather?city=perth")
        assert second_response.status_code == 200
        second_data = second_response.json()

        # data should not be cached
        assert second_data['cached'] is False
        assert second_data['cached_time'] is None


@pytest.mark.asyncio
async def test_different_cities():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/v1/weather?city=sydney")

    # ensure a different city, other than melbourne, provides valid responses
    assert response.status_code == 200
    data = response.json()
    assert 'wind_speed' in data and isinstance(data['wind_speed'], (float, int))
    assert 'temperature_degrees' in data and isinstance(data['temperature_degrees'], (float, int))
