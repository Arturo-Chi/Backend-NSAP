from app.core.base_service import BaseService
from app.models.schemas.secret.controller_merra import URL
from app.models.schemas.secret.controller_merra import DataSet

import xarray as xr

from datetime import datetime, time
from typing import Dict

import earthaccess


class WeatherService(BaseService):

    
    def __init__(self):
        super().__init__("WeatherService")
        

    #Obtiene medición por día y hora
    def getWeatherByDayAtHour(self, lat: float, lon : float, year : str, month : str, day:str, hour : str) -> Dict[str, float]:
        try:

            hh = time.fromisoformat(hour)
            dt = datetime(int(year), int(month), int(day), hh.hour, hh.minute)


            date_hour = f"{year}-{month}-{day}T{hour}"

            auth = earthaccess.login(strategy="interactive", persist="True")

            url = URL.build_URL(year, month, day)

            ds = DataSet.build_DataSet(url)
        
            ds_point = ds.sel(lat = lat, lon = lon, method = "nearest", lev = 72)
            ds_hour = ds_point.sel(time = date_hour)
            variables = ds_hour[["T", "U", "V", "RH","PS"]]

            dictionary = {var: float (variables[var].values) for var in variables.data_vars}

            return dictionary
        
        except Exception as e:
            return self.error(str(e))


    #Obtener listado de variables por las horas del día
    def getWeatherByDay(self, lat: float, lon=float, year=str, month=str, day= str):
        try:
            auth = earthaccess.login(strategy="interactive", persist = "True")
            url = URL.build_URL(year, month, day)

            data = DataSet.build_DataSet(url)




        except Exception as e:
            return self.error(str(e))



