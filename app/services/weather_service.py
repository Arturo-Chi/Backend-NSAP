from app.core.base_service import BaseService
from app.models.schemas.secret.controller_merra import URL
from app.models.schemas.secret.controller_merra import DataSet
from app.models.schemas.weater_response import Weather_Response
import numpy as np

import xarray as xr

from datetime import datetime, time
from typing import Dict, List

import earthaccess

required = ["T", "U", "V", "RH", "PS"]
class WeatherService(BaseService):

    

    def __init__(self):
        super().__init__("WeatherService")


    def kelvinToCelsius(self, kelvin : float):
        
        return    

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

            print(dictionary)
            return dictionary
        
        except Exception as e:
            return self.error(str(e))
        
    


    #Solamente va a devolver la lista de la medición por dia
    def getWeatherByDay(self, lat: float, lon=float, year=str, month=str, day= str) :
        try:
            earthaccess.login(strategy="interactive", persist = "True")
            url = URL.build_URL(year, month, day)

            ds = DataSet.build_DataSet(url)

            ds_point = ds.sel(lat = lat, lon = lon, method="nearest", lev = 72)
                        
            times = ds.time["time"].values

            wph: List[Weather_Response] = []    


            for th in times:

                try:
                    ds_hour = ds_point.sel(time= th)
                except Exception:
                    ds_hour = ds_point.sel(time= th, method = "nearest", tolerance="90min")

                
                sel = ds_hour[required]

                
                t = float(sel["T"].values)
                wu =float(sel["U"].values)
                wv= float(sel["V"].values)
                p = float(sel["PS"].values)
                h = float(sel["RH"].values)

                hour_str = np.datetime_as_string(th, unit='s').split("T")[1]

                wph.append(Weather_Response(
                    hour = hour_str,
                    temperature = t,
                    wind_u = wu,
                    wind_v= wv,
                    atmospheric_pressure = p,
                    humidity = h
                ))

                

            return wph

        except Exception as e:
            return self.error(str(e))



