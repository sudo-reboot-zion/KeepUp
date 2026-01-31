# tools/weather_api_tool.py
"""
Weather API Tool
Fetches real weather data for environmental agent
Uses OpenWeatherMap API (free tier available)
"""
import aiohttp
from typing import Dict, Any, Optional
from config import settings


class WeatherAPITool:
    """
    Fetches weather data from OpenWeatherMap API
    Sign up: https://openweathermap.org/api
    """
    
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY  # Add to config.py
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.air_quality_url = "https://api.openweathermap.org/data/2.5/air_pollution"
    
    async def get_weather(self, location: str) -> Dict[str, Any]:
        """
        Get current weather for a location
        
        Args:
            location: City name (e.g., "Accra, Ghana") or coordinates
            
        Returns:
            Dict with weather data:
            - temperature (°C)
            - feels_like (°C)
            - humidity (%)
            - precipitation (mm)
            - wind_speed (km/h)
            - air_quality (good/moderate/unhealthy)
            - description (cloudy, rainy, etc.)
        """
        
        if not self.api_key:
            # Return mock data if no API key configured
            return self._get_mock_weather()
        
        try:
            # Get coordinates if location is city name
            if "," in location or not any(char.isdigit() for char in location):
                coords = await self._geocode_location(location)
            else:
                # Assume coordinates provided
                lat, lon = map(float, location.split(","))
                coords = {"lat": lat, "lon": lon}
            
            if not coords:
                return self._get_mock_weather()
            
            # Fetch weather data
            weather_data = await self._fetch_weather(coords["lat"], coords["lon"])
            
            # Fetch air quality data
            air_quality_data = await self._fetch_air_quality(coords["lat"], coords["lon"])
            
            # Combine and format
            return self._format_weather_data(weather_data, air_quality_data)
            
        except Exception as e:
            print(f"Weather API error: {str(e)}")
            return self._get_mock_weather()
    
    async def _geocode_location(self, location: str) -> Optional[Dict[str, float]]:
        """Convert city name to coordinates"""
        url = "https://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": location,
            "limit": 1,
            "appid": self.api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        return {"lat": data[0]["lat"], "lon": data[0]["lon"]}
        
        return None
    
    async def _fetch_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """Fetch weather data from API"""
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"  # Celsius
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    return await response.json()
        
        return {}
    
    async def _fetch_air_quality(self, lat: float, lon: float) -> Dict[str, Any]:
        """Fetch air quality data"""
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.air_quality_url, params=params) as response:
                if response.status == 200:
                    return await response.json()
        
        return {}
    
    def _format_weather_data(
        self, 
        weather: Dict[str, Any], 
        air_quality: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format API response into consistent structure"""
        
        # Extract weather data
        main = weather.get("main", {})
        wind = weather.get("wind", {})
        weather_desc = weather.get("weather", [{}])[0]
        rain = weather.get("rain", {})
        
        # Extract air quality (1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor)
        aqi = air_quality.get("list", [{}])[0].get("main", {}).get("aqi", 1)
        air_quality_map = {
            1: "good",
            2: "fair", 
            3: "moderate",
            4: "unhealthy",
            5: "very_unhealthy"
        }
        
        return {
            "temperature": main.get("temp", 25),
            "feels_like": main.get("feels_like", 25),
            "humidity": main.get("humidity", 60),
            "precipitation": rain.get("1h", 0),  # mm in last hour
            "wind_speed": wind.get("speed", 0) * 3.6,  # Convert m/s to km/h
            "air_quality": air_quality_map.get(aqi, "good"),
            "description": weather_desc.get("description", "clear"),
            "condition": weather_desc.get("main", "Clear"),
            "pressure": main.get("pressure", 1013),
            "visibility": weather.get("visibility", 10000) / 1000,  # Convert to km
            "uv_index": None  # Would need separate API call
        }
    
    def _get_mock_weather(self) -> Dict[str, Any]:
        """Return mock weather data when API unavailable"""
        return {
            "temperature": 25,
            "feels_like": 26,
            "humidity": 65,
            "precipitation": 0,
            "wind_speed": 10,
            "air_quality": "good",
            "description": "Partly cloudy",
            "condition": "Clouds",
            "pressure": 1013,
            "visibility": 10,
            "uv_index": None,
            "_mock_data": True
        }


# Convenience function for agents
async def get_weather(location: str) -> Dict[str, Any]:
    """
    Convenience function for agents to get weather
    
    Usage:
        from tools.weather_api_tool import get_weather
        weather = await get_weather("Accra, Ghana")
    """
    tool = WeatherAPITool()
    return await tool.get_weather(location)


# Singleton instance
weather_tool = WeatherAPITool()
