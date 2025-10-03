import xarray as xr
from functools import lru_cache


#Construcción de la URL
class URL:

    #@staticmethod
    def build_URL(yyyy: str, mm: str, dd: str) -> str:

        return (
                f"dap2://goldsmr5.gesdisc.eosdis.nasa.gov/opendap/"
                f"MERRA2/M2I3NVASM.5.12.4/{yyyy}/{mm}/"
                f"MERRA2_400.inst3_3d_asm_Nv.{yyyy}{mm}{dd}.nc4"
        )

class DataSet:
    
        #@staticmethod
        #@lru_cache(maxsize=15)    
        def build_DataSet(url: str):
             ds = xr.open_dataset(url, engine="pydap")
             return ds
             

