import earthaccess
from fastapi import FastAPI
#from app.routes.clima import router as clima_router
from app.routes.weather_route import router as weather_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:4200",
    "http://10.0.32.21:4200",
    "*"
    
]
     


app = FastAPI(title="Clim Mate ")
#auth = earthaccess.login(strategy="interactive", persist=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


app.include_router(weather_router)