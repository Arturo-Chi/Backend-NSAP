
import xarray as xr
from app.core.base_service import BaseService

class ClimaService(BaseService):

    def __init__(self):
        super().__init__("ClimaService")


    def obtener_clima(self, lat: float, lon: float, fecha: str):
        try:
            url = "https://opendap.nasa.gov/some_dataset.nc"
            ds = xr.open_dataset(url)
            temp = ds["temperature"].sel(lat=lat, lon=lon, time=fecha, method = "nearest")
            return self.success({
                "lat":lat,
                "lon": lon,
                "temperatura":float(temp).values

        })   

        except Exception as e:
            return self.error(str(e))
