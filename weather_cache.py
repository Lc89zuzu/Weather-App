import time
import json
import os

# Weather Cache class to store and retrieve weather data with expiry time
class WeatherCache:
    def __init__(self, cache_file='weather_cache.json', expiry_time=3600):
        self.cache_file = cache_file
        self.expiry_time = expiry_time
        self.cache = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def get(self, key):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.expiry_time:
                return data
        return None

    def set(self, key, value):
        self.cache[key] = (value, time.time())
        self.save_cache()

def get_cached_weather(city, fetch_weather_func):
    cache = WeatherCache()
    cached_data = cache.get(city)
    if cached_data:
        return cached_data
    
    fresh_data = fetch_weather_func(city)
    cache.set(city, fresh_data)
    return fresh_data