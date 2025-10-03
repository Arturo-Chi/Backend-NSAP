from app.core.base_service import BaseService
from app.models.schemas.secret.controller_merra import URL
from app.models.schemas.secret.controller_merra import DataSet
from app.models.schemas.weater_response import Weather_Response
from app.models.schemas.weater_response import MeditionByYear


import numpy as np

import xarray as xr

from datetime import datetime, time
from typing import Dict, List

import earthaccess

required = ["T", "U", "V", "RH", "PS"]
class WeatherService(BaseService):

    

    def __init__(self):
        super().__init__("WeatherService")


    def kelvinToCelsius(kelvin : float):
        return kelvin-275

    #Obtiene medición por día y hora
    def getWeatherByDayAtHour(self, lat: float, lon : float, year : str, month : str, day:str, hour : str) -> Dict[str, float]:
        try:

            hh = time.fromisoformat(hour)
            dt = datetime(int(year), int(month), int(day), hh.hour, hh.minute)


            date_hour = f"{year}-{month}-{day}T{hour}"

            

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
        
    
    def getWeatherHistory(self, lat: float, lon: float, year: int, month: int, day: int):
        try:
            history: list[MeditionByYear] = []

           
            n_years = 3

            for k in range(1, n_years + 1):
                y = year - k

         
                url = URL.build_URL(str(y), f"{month:02d}", f"{day:02d}")
                ds = DataSet.build_DataSet(url)

          
                ds_point = ds.sel(lat=lat, lon=lon, method="nearest", lev=72)

          
                missing = [v for v in required if v not in ds_point.data_vars]
                if missing:
                    return self.error(f"Faltan variables en dataset {y}-{month:02d}-{day:02d}: {missing}")

             
                times = ds_point["time"].values 

                day_measures: list[Weather_Response] = []

                for ts in times:
                   
                    try:
                        ds_hour = ds_point.sel(time=ts)
                    except Exception:
                        ds_hour = ds_point.sel(time=ts, method="nearest", tolerance="90min")

                    sel = ds_hour[required]

                    T  = float(sel["T"].to_numpy().item())
                    U  = float(sel["U"].to_numpy().item())
                    V  = float(sel["V"].to_numpy().item())
                    RH = float(sel["RH"].to_numpy().item())
                    PS = float(sel["PS"].to_numpy().item())

                    
                    hour_str = np.datetime_as_string(ts, unit='s').split("T")[1]

                    day_measures.append(Weather_Response(
                        hour=hour_str,
                        temperature=T,
                        wind_u=U,
                        wind_v=V,
                        atmospheric_pressure=PS,
                        humidity=RH
                    ))

                
                history.append(MeditionByYear(
                    year=f"{y}",
                    month=f"{month:02d}",
                    measurements=day_measures
                ))

            return history

        except Exception as e:
            return self.error(str(e))


    #Solamente va a devolver la lista de la medición por dia
    def getWeatherByDay(self, lat: float, lon=float, year=str, month=str, day= str) :
        try:
           
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



