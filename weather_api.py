import requests
from datetime import datetime, timedelta

# Weather API
weather_cache = {}

def get_cached_weather(city, fetch_func, cache_duration=timedelta(minutes=30)):
    current_time = datetime.now()
    if city in weather_cache:
        cached_time, cached_data = weather_cache[city]
        if current_time - cached_time < cache_duration:
            return cached_data
    
    fresh_data = fetch_func(city)
    weather_cache[city] = (current_time, fresh_data)
    return fresh_data

def fetch_current_weather(city):
    return get_cached_weather(city, lambda c: _fetch_weather_from_api(c))

def _fetch_weather_from_api(city):
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    geo_response = requests.get(geocoding_url)
    geo_data = geo_response.json()
    
    if not geo_data.get('results'):
        return f"City '{city}' not found."
    
    lat, lon = geo_data['results'][0]['latitude'], geo_data['results'][0]['longitude']
    
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m,precipitation"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    
    current = weather_data['current_weather']
    hourly = weather_data['hourly']
    
    # Find the closest time in hourly data
    current_time = datetime.fromisoformat(current['time'])
    closest_time = min(hourly['time'], key=lambda t: abs(datetime.fromisoformat(t) - current_time))
    current_index = hourly['time'].index(closest_time)
    
    return {
        'temperature': current['temperature'],
        'windspeed': current['windspeed'],
        'humidity': hourly['relativehumidity_2m'][current_index],
        'precipitation': hourly['precipitation'][current_index]
    }

# Remove or comment out the fetch_5day_forecast function if you're not using it