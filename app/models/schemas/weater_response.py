
from pydantic import BaseModel
from typing import List


class Weather_Response (BaseModel):
    hour: str = ""
    temperature : float = 0.0
    wind_u : float = 0.0
    wind_v: float = 0.0
    atmospheric_pressure: float = 0.0
    humidity : float = 0.0






class WeatherPerDay_Response(BaseModel):
    latitude: float = 0.0
    longitude: float = 0.0
    date: str = ""
    hours: List[Weather_Response]