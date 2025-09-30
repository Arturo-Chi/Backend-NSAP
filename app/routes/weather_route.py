from app.core.base_route import BaseRoute
from app.services.weather_service import WeatherService
from app.models.schemas.weater_response import WeatherResponse

ws = WeatherService()

route = BaseRoute(prefix="/api", tag="ApiWeather")
router = route.get_router()

@router.get("/weather", response_model= WeatherResponse)
def getWeatherPerDay():
    data_set = ws.getWeatherByDayAtHour()
    return WeatherResponse(
        temperature = data_set["T"],
        wind_u = data_set["U"],
        wind_v = data_set["V"],
        atmospheric_pressure = data_set["PS"],
        humidity = data_set["RH"]
    )


