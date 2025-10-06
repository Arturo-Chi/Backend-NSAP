from app.core.base_service import BaseService
from app.models.schemas.secret.controller_merra import URL
from app.models.schemas.secret.controller_merra import DataSet
from app.models.schemas.weater_response import Weather_Response
from app.models.schemas.weater_response import MeditionByYear
from app.models.schemas.weater_response import AverageWeather_Response
import random
import math

import numpy as np

import xarray as xr

from datetime import datetime, time
from typing import Dict, List

import earthaccess

required = ["T", "U", "V", "RH", "PS"]
class WeatherService(BaseService):

    def __init__(self):
        super().__init__("WeatherService")

     

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


                    speed = math.sqrt(U**2 + V**2)
                    direction = (math.degrees(math.atan2(-U, -V)) + 360) % 360
                    
                    hour_str = np.datetime_as_string(ts, unit='s').split("T")[1]

                    day_measures.append(Weather_Response(
                        hour=hour_str,
                        temperature=T-273.15,
                        wind_speed=speed,
                        wind_direction=direction,
                        atmospheric_pressure=PS/100,
                        humidity=RH
                    ))

                
                history.append(MeditionByYear(
                    year=f"{y}",
                    month=f"{month:02d}",
                    measurements=day_measures
                ))
                print(history)

            return history

        except Exception as e:
            return self.error(str(e))

    def getWeatherHistoryAverage(
    self,
    lat: float, lon: float,
    year: int, month: int, day: int,
    umbral_temp: float,   
    umbral_windv: float, 
    umbral_ps: float,     
    umbral_h: float       
    ) -> AverageWeather_Response:
        try:
                
                n_years = 3

                temps_daily, hum_daily, ps_daily, spd_daily = [], [], [], []

                over_temperature = over_windvVelocity = over_atmps = over_humity = 0
                under_temperature = under_windvVelocity = under_atmps = under_humity = 0

                for k in range(1, n_years + 1):
                    y = year - k
                    print(year)
                    url = URL.build_URL(str(y), f"{month:02d}", f"{day:02d}")
                    ds  = DataSet.build_DataSet(url)
                    ds_point = ds.sel(lat=lat, lon=lon, method="nearest", lev=72)

                    missing = [v for v in required if v not in ds_point.data_vars]
                    if missing:
                    
                        continue

                    times = ds_point["time"].values

                    T_list, RH_list, PS_list, SPD_list = [], [], [], []

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

                        speed = math.hypot(U, V)                  

                        T_list.append(T - 273.15)   
                        RH_list.append(RH * 100.0)  
                        PS_list.append(PS / 100.0)  
                        SPD_list.append(speed)      

                    if not T_list:
                        continue

                    t_mean   = float(np.mean(T_list))    
                    h_mean   = float(np.mean(RH_list))   
                    ps_mean  = float(np.mean(PS_list))   
                    spd_mean = float(np.mean(SPD_list))  

                    temps_daily.append(t_mean)
                    hum_daily.append(h_mean)
                    ps_daily.append(ps_mean)
                    spd_daily.append(spd_mean)

                    
                    if t_mean > umbral_temp:   over_temperature  += 1
                    elif t_mean < umbral_temp: under_temperature += 1

                    if spd_mean > umbral_windv:   over_windvVelocity  += 1
                    elif spd_mean < umbral_windv: under_windvVelocity += 1

                    if ps_mean > umbral_ps:   over_atmps  += 1
                    elif ps_mean < umbral_ps: under_atmps += 1

                    if h_mean > umbral_h:   over_humity  += 1
                    elif h_mean < umbral_h: under_humity += 1

            

                temperature_avg = float(np.mean(temps_daily))  # °C
                humidity_avg    = float(np.mean(hum_daily))    # %
                pressure_avg    = float(np.mean(ps_daily))     # hPa
                wind_speed_avg  = float(np.mean(spd_daily))    # m/s

                probability = (
                    0.02022 * humidity_avg
                    - 0.30598 * wind_speed_avg
                    - 0.03011 * (pressure_avg - 1000.0)
                    + 32.50
                )
                probability = max(0.0, min(100.0, probability))

                
                over_temperature_p   = over_temperature   / n_years
                under_temperature_p  = under_temperature  / n_years
                over_windvVelocity_p = over_windvVelocity / n_years
                under_windvVelocity_p= under_windvVelocity/ n_years
                over_atmps_p         = over_atmps         / n_years
                under_atmps_p        = under_atmps        / n_years
                over_humity_p        = over_humity        / n_years
                under_humity_p       = under_humity       / n_years

                return AverageWeather_Response(
                    temperature=round(temperature_avg, 2),          # °C
                    wind_speed=round(wind_speed_avg, 2),            # m/s (o conviértelo a km/h si prefieres)
                    atmospheric_pressure=round(pressure_avg, 2),    # hPa
                    humidity=round(humidity_avg, 2),                # %
                    rain_probability=round(probability, 2),         # %

                    over_temperature=over_temperature_p,
                    over_windvVelocity=over_windvVelocity_p,
                    over_atmps=over_atmps_p,
                    over_humity=over_humity_p,
                    under_temperature=under_temperature_p,
                    under_windvVelocity=under_windvVelocity_p,
                    under_atmps=under_atmps_p,
                    under_humity=under_humity_p
                )

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

                speed = math.sqrt(wu**2 + wv**2)
                direction = (math.degrees(math.atan2(-wu, -wv))+360)%360

                wph.append(Weather_Response(
                    hour = hour_str,
                    temperature = t-273.15,
                    wind_speed = speed,
                    wind_direction= direction,
                    atmospheric_pressure = p/100,
                    humidity = h
                ))
                print(wph)

                

            return wph

        except Exception as e:
            return self.error(str(e))



