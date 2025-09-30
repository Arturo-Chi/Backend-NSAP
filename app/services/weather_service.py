from app.core.base_service import BaseService
import xarray as xr
import earthaccess


class WeatherService(BaseService):
    
    super()._init_("WeatherService")


    def getWeatherByDayAtHour(self, lat: float, lon = float, year = str, month = str, day=str, hour = str):
        try:
            auth = earthaccess.login(strategy="interactive", persist="True")
            url = "dap2://goldsmr5.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2I3NVASM.5.12.4/"+year+"/"+month+"/MERRA2_400.inst3_3d_asm_Nv."+year+month+day+".nc4"
            ds = xr.open_dataset(url, engine="pydap")
            date_time = year,"-",month,"-",day,"T",hour
            definition = ds.sel(lat=lat, lon = lon, method="nearest", time= date_time, lev= 72)
            valores = definition[["T", "U", "V", "RH", "PS"]]

            dicc = {var: float (valores[var].values) for var in valores.data_vars}
            return dicc


        except Exception as e:
            return self.error(str(e))


    def getWeatherByDay(self, lat: float, lon=float, year=str, month=str, day= str):
        try:
            print("Este es el método para ver todas las mediciones de un día")

        except Exception as e:
            return self.error(str(e))



