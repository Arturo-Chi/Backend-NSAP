
from pydantic import BaseModel
from typing import List


class Weather_Response (BaseModel):
    hour: str = ""
    temperature : float = 0.0
    wind_speed : float = 0.0
    wind_direction: float = 0.0
    atmospheric_pressure: float = 0.0
    humidity : float = 0.0


class WeatherPerDay_Response(BaseModel):
    latitude: float = 0.0
    longitude: float = 0.0
    date: str = ""
    hours: List[Weather_Response]


class WeatherDay_Response(BaseModel):
    hours: List[Weather_Response]




class MeditionByYear(BaseModel):
    year: int = 0,
    month: int = 0,
    measurements: List[Weather_Response]


class WeatherHistory_Response(BaseModel):
    latitude : float = 0
    longitude: float = 0
    results: List[MeditionByYear]

class AverageWeather_Response(BaseModel) :
    temperature: float = 0
    wind_speed : float = 0
    atmospheric_pressure: float = 0
    humidity: float = 0
    rain_probability: float = 0
    over_temperature: float = 0
    over_windvVelocity: float = 0
    over_atmps: float = 0
    over_humity: float = 0
    under_temperature: float = 0
    under_windvVelocity: float = 0
    under_atmps: float = 0
    under_humity: float = 0