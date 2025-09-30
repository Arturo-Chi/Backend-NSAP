
from pydap import BaseModel


class WeatherResponse (BaseModel):
    temperature : float
    wind_u : float
    wind_v: float
    atmospheric_pressure: float
    humidity : float