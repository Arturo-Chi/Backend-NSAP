from fastapi import Query, HTTPException
from app.core.base_route import BaseRoute
from app.services.weather_service import WeatherService
from app.models.schemas.weater_response import Weather_Response
from app.models.schemas.weater_response import WeatherPerDay_Response


ws = WeatherService()

route = BaseRoute(prefix="/api", tag="ApiWeather")
router = route.get_router()
required = ["T", "U", "V", "RH", "PS"]



@router.get("/")
def hello_world():
   return {
       "message" : "Hello World"
   }


@router.get("/weather", response_model= Weather_Response)
def get_WeatherByTime(
    lat : float = Query(...),
    lon : float = Query(...),
    year : str = Query(..., regex= r"^\d{4}$"),
    month : str = Query(..., regex= r"^\d{2}$"), 
    day : str = Query(..., regex= r"^\d{2}$"),
    hour : str = Query(..., description="HH:MM:SS")
):
    data_set = ws.getWeatherByDayAtHour(lat=lat, lon = lon, year = year, month=month, day = day, hour = hour)
    
    if isinstance(data_set, dict) and data_set.get("status") == "error":
        raise HTTPException(status_code=502, detail=data_set.get("message","Upstream error"))
    
    try:
        return Weather_Response(
            hour = hour,
            temperature = data_set["T"],
            wind_u = data_set["U"],
            wind_v = data_set["V"],
            atmospheric_pressure = data_set["PS"],
            humidity = data_set["RH"]
        )
    except Exception as e:
        raise HTTPException(status_code = 502, detail = f"variable faltante en: {str(e)}")
    
    #, 
@router.get("/weather/date", response_model= WeatherPerDay_Response)
def get_WeatherAtDate(lat: float, lon: float, year: str, month: str, day:str):

    weather_list = ws.getWeatherByDay(lat = lat, lon = lon, year= year, month = month, day = day)

    if isinstance(weather_list, dict) and weather_list.get("status")=="error":
        raise HTTPException(status_code=502, detail = weather_list.get("message", "Upstream error"))
    if not weather_list:
        raise HTTPException(status_code=404, detail="Lista vacía")



    return WeatherPerDay_Response(
        latitude = lat,
        longitude = lon,
        date = f"{year}-{month}-{day}",
        hours = weather_list
    )



    
    
    


     
#
#    return WeatherPerDay_Response(  
#        latitude = lat,
#        longitude = lon,
#        date = f"{year}/{month}/{day}",
#        hours = data

#    )

    


