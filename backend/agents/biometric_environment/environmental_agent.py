# agents/biometric_environment/environmental_agent.py
"""
Environmental Agent
Adapts workouts based on weather, location, and environmental factors
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent


class EnvironmentalAgent(BaseAgent):
    """
    Monitors environmental conditions and adapts workouts accordingly
    
    Responsibilities:
    - Check weather conditions
    - Recommend indoor/outdoor workout adjustments
    - Account for temperature, humidity, air quality
    - Suggest alternative locations if needed
    """
    
    def __init__(self):
        super().__init__(
            name="Environmental Agent",
            description="Environmental science expert who adapts workouts to conditions",
            model="llama-3.3-70b-versatile",
            requires_user_context=False
        )
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze environmental conditions and recommend adaptations
        
        Input:
            - location: str (city or coordinates)
            - planned_workout: Dict
            - user_preferences: Dict
            
        Returns:
            - conditions: Dict (weather, air quality)
            - recommendations: List[str]
            - workout_modifications: List[Dict]
            - safe_to_proceed: bool
            - confidence: float
        """
        
        location = input_data.get("location", "unknown")
        planned_workout = input_data.get("planned_workout", {})
        preferences = input_data.get("user_preferences", {})
        
        # Get weather data (mock for now - you'll integrate real API)
        weather = await self._get_weather_data(location)
        
        # Assess conditions
        conditions = {
            "temperature": weather.get("temperature", 25),
            "feels_like": weather.get("feels_like", 25),
            "humidity": weather.get("humidity", 60),
            "precipitation": weather.get("precipitation", 0),
            "air_quality": weather.get("air_quality", "good"),
            "wind_speed": weather.get("wind_speed", 5)
        }
        
        # Build prompt
        system_prompt = """You are an environmental science expert specializing in workout safety.

Your role:
- Assess if conditions are safe for planned workout
- Recommend modifications for extreme weather
- Suggest indoor alternatives when needed
- Account for user preferences and tolerance

Safety thresholds:
- Heat: >32°C = reduce intensity, >38°C = move indoors
- Cold: <-10°C = move indoors or reduce duration
- Humidity: >80% = increased dehydration risk
- Air Quality: "Unhealthy" or worse = move indoors
- Precipitation: Heavy rain = safety risk outdoors
- Wind: >40 km/h = outdoor workout dangerous

Respond with JSON:
{
    "safe_to_proceed": true,
    "conditions_summary": "Pleasant weather, ideal for outdoor exercise",
    "recommendations": [
        "Bring extra water - moderate humidity",
        "Apply sunscreen - UV index is high"
    ],
    "workout_modifications": [
        {
            "original": "30min outdoor run",
            "modified": "30min run with hydration breaks every 10min",
            "rationale": "Temperature is warm but safe with proper hydration"
        }
    ],
    "alternative_location": "Indoor gym if conditions worsen",
    "confidence": 0.85
}"""
        
        workout_desc = f"{planned_workout.get('type', 'workout')} - {planned_workout.get('duration', '30min')}"
        workout_location = planned_workout.get('location', 'outdoor')
        indoor_preference = preferences.get("prefers_indoor", False)
        
        user_prompt = f"""Analyze environmental conditions for workout:

WEATHER CONDITIONS:
- Temperature: {conditions['temperature']}°C (feels like {conditions['feels_like']}°C)
- Humidity: {conditions['humidity']}%
- Precipitation: {conditions['precipitation']}mm
- Air Quality: {conditions['air_quality']}
- Wind: {conditions['wind_speed']} km/h

PLANNED WORKOUT:
- Type: {workout_desc}
- Location: {workout_location}

USER PREFERENCES:
- Prefers Indoor: {indoor_preference}
- Heat Tolerance: {preferences.get('heat_tolerance', 'moderate')}
- Cold Tolerance: {preferences.get('cold_tolerance', 'moderate')}

Your task:
1. Assess if conditions are safe for outdoor workout
2. Recommend specific modifications if needed
3. Suggest indoor alternative if unsafe
4. Account for user preferences and tolerance
5. Provide clear, actionable guidance

Generate JSON response."""
        
        response = await self._call_llm(
            system_prompt=system_prompt, 
            user_prompt=user_prompt, 
            temperature=0.2,  # Low temperature for safety-critical decisions
            max_tokens=1000
        )
        
        result = self._parse_json_response(response)
        
        # Add conditions to result
        result["conditions"] = conditions
        result["location"] = location
        result["agent_name"] = self.name
        
        return result
    
    async def _get_weather_data(self, location: str) -> Dict[str, Any]:
        """
        Get weather data for location
        Integrate with real weather API (OpenWeatherMap, WeatherAPI, etc.)
        """
        from tools.weather_api_tool import get_weather
        return await get_weather(location)



environmental_agent = EnvironmentalAgent()